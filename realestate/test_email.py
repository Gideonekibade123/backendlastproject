import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate.settings")
django.setup()

from django.core.mail import send_mail

send_mail(
    "Test Email",
    "Hello from Django",
    "gekibade@gmail.com",
    ["gekibade@gmail.com"],
    fail_silently=False,
)

send_mail(
    "New Enquiry",
    "Someone just contacted you about a property",
    settings.DEFAULT_FROM_EMAIL,
    ["admin@gmail.com"]
)


print("Email sent!")