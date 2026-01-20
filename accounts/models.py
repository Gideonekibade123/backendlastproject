from listings.models import PropertyListing

from django.db import models
from django.contrib.auth.models import User

    
# Optional Profile model to store extra info about users
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    payment_completed = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

