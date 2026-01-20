from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.core.signing import Signer

signer = Signer()

def send_verification_email(user, request):
    token = signer.sign(user.pk)  # create a signed token
    verification_url = request.build_absolute_uri(
        reverse('accounts:verify-email', args=[token])
    )

    subject = "Verify your email"
    message = f"Hi {user.username},\n\nPlease verify your email by clicking the link below:\n\n{verification_url}\n\nThank you!"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
