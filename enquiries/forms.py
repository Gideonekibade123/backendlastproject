from django import forms
from .models import SellerMessage

class SellerMessageForm(forms.ModelForm):
    class Meta:
        model = SellerMessage
        fields = ['sender_name', 'sender_email', 'message']