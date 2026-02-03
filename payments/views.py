from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
from .models import Payment
import requests

class PaystackInitializeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount")
        if not amount:
            return Response({"status": False, "message": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Create payment in DB with pending status
        payment = Payment.objects.create(
            user=request.user,
            amount=amount,
            reference=f"REF-{request.user.id}-{Payment.objects.count() + 1}"
        )

        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}

        # payload = {
        #     "email": request.user.email,
        #     "amount": amount,
        #     "reference": payment.reference,
        #     "callback_url": f"http://127.0.0.1:5500/payment_success.html?reference={payment.reference}"
        # }
         
        payload = {
    "email": request.user.email,
    "amount": amount,
    "reference": payment.reference,
    "callback_url": f"https://realestatefrontend.netlify.app/payment_successful.html?reference={payment.reference}"  # <-- new
         }




        r = requests.post("https://api.paystack.co/transaction/initialize", headers=headers, json=payload)
        response_data = r.json()

        return Response(response_data)

class PaystackVerifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reference):
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        r = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)
        resp = r.json()

        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            return Response({"status": "error", "message": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        if resp["status"] and resp["data"]["status"] == "success":
            payment.status = "success"
            payment.save()
            return Response({"status": "success", "message": "Payment verified and updated"})
        else:
            payment.status = "failed"
            payment.save()
            return Response({"status": "failed", "message": "Payment failed"})
