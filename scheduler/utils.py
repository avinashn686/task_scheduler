# utils.py (or views.py)

from mailjet_rest import Client
from django.conf import settings
from django.core.mail import BadHeaderError


def send_mail_with_mailjet(subject, message, from_email, to_email):
    mailjet = Client(
        auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version="v3.1"
    )

    data = {
        "Messages": [
            {
                "From": {"Email": from_email, "Name": "Your Name"},
                "To": [{"Email": to_email, "Name": "Recipient Name"}],
                "Subject": subject,
                "TextPart": message,
            }
        ]
    }

    result = mailjet.send(data=data)
    return result.status_code, result.json()
