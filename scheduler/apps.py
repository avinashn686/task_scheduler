from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        from .tasks import create_reminder_periodic_task
        create_reminder_periodic_task()  # Create or update the periodic task on app startup
