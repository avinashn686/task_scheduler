from django.shortcuts import render
from datetime import datetime, timedelta
from rest_framework import status, viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from scheduler.serializers import TaskSerializer, UserSerializer
from scheduler.models import Task
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .tasks import send_task_reminders


class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        keyword = self.request.query_params.get("q", "").strip().lower()
        if "@" in keyword:
            return User.objects.filter(email__iexact=keyword)
        else:
            return User.objects.filter(
                first_name__icontains=keyword
            ) | User.objects.filter(last_name__icontains=keyword)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"detail": "Successfully logged out."})
        except Exception as e:
            return Response({"detail": "Logout failed."}, status=400)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(user=user)

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user)
        if task.reminder_time:
            send_task_reminders.apply_async((task.id,), eta=task.reminder_time)

    def perform_update(self, serializer):
        task = serializer.save()
        if task.completed:
            task.time_spent += timezone.now() - task.created_at
            task.save()
        if task.reminder_time:
            send_task_reminders.apply_async((task.id,), eta=task.reminder_time)


class TimeTrackingView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, pk=None):
        task = Task.objects.get(pk=pk, user=request.user)
        time_spent_str = request.data.get("time_spent")

        if task and time_spent_str:
            # Parse the time_spent string to timedelta
            try:
                # Assuming time_spent is in "HH:MM:SS" format
                time_parts = list(map(int, time_spent_str.split(':')))
                if len(time_parts) == 3:  # HH:MM:SS
                    time_spent = timedelta(hours=time_parts[0], minutes=time_parts[1], seconds=time_parts[2])
                elif len(time_parts) == 2:  # MM:SS
                    time_spent = timedelta(minutes=time_parts[0], seconds=time_parts[1])
                elif len(time_parts) == 1:  # SS
                    time_spent = timedelta(seconds=time_parts[0])
                else:
                    return Response({"error": "Invalid time format."}, status=status.HTTP_400_BAD_REQUEST)

                # Update the task's time_spent
                task.time_spent += time_spent
                task.save()
                return Response(
                    {"message": "Time tracked successfully!"}, status=status.HTTP_200_OK
                )
            except ValueError:
                return Response({"error": "Invalid time format."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
