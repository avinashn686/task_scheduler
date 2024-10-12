from django.contrib import admin

# Register your models here.
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "due_date",
        "reminder_time",
        "completed",
        "created_at",
        "updated_at",
        "time_spent",
    )
    list_filter = ("user", "completed", "due_date")
    search_fields = ("title", "description", "user__username")
    ordering = ("-created_at",)
    date_hierarchy = "due_date"


admin.site.register(Task, TaskAdmin)
