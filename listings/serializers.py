from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    # Show owner's username in API response
    owner = serializers.ReadOnlyField(source='owner.username')

class Meta:
        model = Listing
        fields = [
            'id',
            'title',
            'description',
            'price',
            'category',
            'location',
            'image',
            'owner',
            'created_at',
        ]