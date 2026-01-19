# from django.db import models
# from django.contrib.auth.models import User
# from listings.models import Listing

# class Enquiries(models.Model):
#     listing = models.ForeignKey(
#         Listing,
#         on_delete=models.CASCADE,
#         related_name="enquiries"
#     )
#     sender = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="sent_enquiries"
#     )


# class SellerMessage(models.Model):
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="messages")


#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Enquiry from {self.sender.username} for {self.listing.title}"
    




# from django.db import models
# from django.contrib.auth.models import User
# from listings.models import Listing  # Assuming your Listing model is here

# class SellerMessage(models.Model):
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="messages")
#     sender_name = models.CharField(max_length=100)
#     sender_email = models.EmailField()
#     message = models.TextField()
#     sent_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Message from {self.sender_name} to {self.listing.owner.username}"






from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing  # adjust if your app name is different


class SellerMessage(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='enquiries'
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender_name} to {self.seller.username}"




