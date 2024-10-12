from rest_framework import serializers
from django.contrib.auth.models import User
from scheduler.models import Task


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):
    time_spent = serializers.DurationField(required=False, allow_null=True)
    reminder_time = serializers.DateTimeField(required=False, allow_null=True)
    due_date = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "user",
            "created_at",
            "updated_at",
            "due_date",
            "reminder_time",
            "completed",
            "time_spent",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        validated_data.pop("user", None)

        return Task.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
