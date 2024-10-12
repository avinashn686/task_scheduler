from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from scheduler.models import Task
from django.utils import timezone
from datetime import timedelta


class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "password": "password123",
            "email": "testuser@example.com",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        url = reverse("user-registration-list")
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_user_login(self):
        url = reverse("login")
        data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_user_logout(self):
        # Log the user in first
        login_url = reverse("login")
        login_data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(login_url, login_data)
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Logout
        logout_url = reverse("logout")
        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Successfully logged out.")


class TaskTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="taskuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        url = reverse("task-list")
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "due_date": timezone.now() + timedelta(days=1),
        }
        response = self.client.post(url, task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, "Test Task")

    def test_list_user_tasks(self):
        # Create two tasks for the authenticated user
        Task.objects.create(
            title="Task 1",
            description="Task 1 desc",
            user=self.user,
            due_date=timezone.now() + timedelta(days=1),
        )
        Task.objects.create(
            title="Task 2",
            description="Task 2 desc",
            user=self.user,
            due_date=timezone.now() + timedelta(days=2),
        )

        url = reverse("task-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_task(self):
        task = Task.objects.create(
            title="Old Task",
            description="Old description",
            user=self.user,
            due_date=timezone.now() + timedelta(days=2),
        )
        url = reverse("task-detail", args=[task.id])
        updated_data = {
            "title": "Updated Task",
            "description": "Updated description",
        }
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, "Updated Task")

    def test_delete_task(self):
        task = Task.objects.create(
            title="Task to delete",
            description="This task will be deleted",
            user=self.user,
            due_date=timezone.now() + timedelta(days=2),
        )
        url = reverse("task-detail", args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
