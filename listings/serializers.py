from rest_framework import serializers
from .models import Listing, ListingImage

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image']

class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    seller_name = serializers.CharField(source='owner.username', read_only=True)  # ✅ added seller_name
    images = ListingImageSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id',
            'title',
            'description',
            'price',
            'phone',
            'category',
            'location',
            'images',        # multiple images
            'owner',         # backend username
            'seller_name',   # for frontend display
            'is_sold',
            'created_at',
        ]
        read_only_fields = ['id', 'owner', 'seller_name', 'is_sold', 'created_at']





