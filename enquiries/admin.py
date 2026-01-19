
# from django.contrib import admin
# from .models import Enquiries

# class EnquiriesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'sender', 'listing', 'content', 'created_at')
#     list_filter = ('created_at',)
#     search_fields = ('sender__username', 'listing__title', 'content')

# admin.site.register(Enquiries, EnquiriesAdmin)



# from django.contrib import admin
# from .models import Enquiries

# @admin.register(Enquiries)
# class EnquiriesAdmin(admin.ModelAdmin):
#     list_display = ("id", "listing", "sender", "content", "created_at")
#     list_filter = ("created_at",)
#     search_fields = ("sender__username", "listing__title", "content")



from django.contrib import admin
from .models import SellerMessage

@admin.register(SellerMessage)
class SellerMessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'sender_email', 'seller', 'created_at')
    search_fields = ('sender_name', 'sender_email', 'message')




