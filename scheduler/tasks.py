import logging
from celery import shared_task
from django.utils import timezone
from scheduler.models import Task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from mailjet_rest import Client
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)


@shared_task
def send_task_reminders(task_id):
    try:
        now = timezone.now()
        task = Task.objects.get(id=task_id)

        if task.reminder_time and task.reminder_time <= now and not task.completed:
            mailjet = Client(
                auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET),
                version="v3.1",
            )

            data = {
                "Messages": [
                    {
                        "From": {
                            "Email": "avinashn686@gmail.com",  # Replace with your verified sender email
                            "Name": "Avinash",
                        },
                        "To": [{"Email": task.user.email, "Name": task.user.username}],
                        "Subject": f"Reminder: Task '{task.title}' is due soon!",
                        "TextPart": f"Dear {task.user.username}, your task '{task.title}' is due on {task.due_date}.",
                    }
                ]
            }

            result = mailjet.send.create(data=data)

            if result.status_code == 200:
                logger.info(
                    f"Reminder email sent for task: {task.title} to {task.user.email}"
                )
            else:
                logger.error(
                    f"Failed to send email for task '{task.title}': {result.status_code}, {result.json()}"
                )

    except Task.DoesNotExist:
        logger.error(f"Task with ID {task_id} does not exist.")
    except Exception as e:
        logger.error(f"Error sending email for task ID {task_id}: {str(e)}")


def create_reminder_periodic_task():
    # Create a schedule that runs every 15 minutes
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=15, period=IntervalSchedule.MINUTES
    )

    task_name = "Send Task Reminders"
    try:
        PeriodicTask.objects.update_or_create(
            interval=schedule,
            name=task_name,
            defaults={
                "task": "scheduler.tasks.send_task_reminders",  # The task name from tasks.py
                "enabled": True,
            },
        )
        logger.info(f"Periodic task '{task_name}' created/updated successfully.")
    except Exception as e:
        logger.error(f"Error creating/updating periodic task '{task_name}': {e}")
