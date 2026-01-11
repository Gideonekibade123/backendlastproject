# from django.contrib import admin
# from .models import Listing, ListingImage


# class ListingImageInline(admin.TabularInline):
#     model = ListingImage
#     extra = 1


# @admin.register(Listing)
# class ListingAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'price', 'location', 'owner', 'created_at')
#     list_filter = ('category', 'created_at')
#     search_fields = ('title', 'location', 'owner__username')
#     inlines = [ListingImageInline]


# @admin.register(ListingImage)
# class ListingImageAdmin(admin.ModelAdmin):
#     list_display = ('listing', 'id')






from django.contrib import admin
from .models import Listing, ListingImage


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'location', 'owner', 'created_at')
    inlines = [ListingImageInline]


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'image')
