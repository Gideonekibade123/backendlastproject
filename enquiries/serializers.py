# from rest_framework import serializers
# from .models import SellerMessage
# from listings.models import Listing

# class SellerMessageSerializer(serializers.ModelSerializer):
#     sender = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )

#     class Meta:
#         model = SellerMessage
#         fields = [
#             "id",
#             "listing",
#             "sender_name",
#             "sender_email",
#             "message",
#             "created_at"]
#         read_only_fields = ["id", "created_at"]




from rest_framework import serializers
from .models import SellerMessage


class SellerMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerMessage
        fields = [
            'id',
            'listing',
            'sender_name',
            'sender_email',
            'message',
            'created_at',
        ]
        read_only_fields = ['created_at']


    