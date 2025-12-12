#from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Listing(models.Model):
    # Category choices
    CATEGORY_CHOICES = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('buy', 'Buy'),
    )

    # Listing fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='listing_images/', null=True, blank=True)

    # Relationship with User
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.category} - {self.location}"
