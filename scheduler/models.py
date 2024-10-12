from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    reminder_time = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    time_spent = models.DurationField(default=timedelta(0))

    def __str__(self):
        return self.title
