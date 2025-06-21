from django.urls import path
from users.views import PaymentListAPIView, UserProfileAPIView

app_name = "users"

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("me/", UserProfileAPIView.as_view(), name="user-profile"),
]
