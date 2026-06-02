import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate.settings")
django.setup()

from django.core.mail import send_mail

send_mail(
    "Test Email",
    "Hello from Django",
    "gekibade@gmail.com",
    ["your_email@example.com"],
    fail_silently=False,
)

print("Email sent!")