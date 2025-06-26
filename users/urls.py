from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (
    PaymentListAPIView,
    RegisterView,
    UserProfileAPIView,
    UserRetrieveUpdateView,
    CreatePaymentView,
    PaymentStatusView
)

from .views import UserViewSet

app_name = "users"

router = DefaultRouter()
router.register("", UserViewSet, basename="user")

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("me/", UserProfileAPIView.as_view(), name="user-profile"),
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
    path("users/<int:pk>/", UserRetrieveUpdateView.as_view(), name="user-detail"),
    path("payments/create/", CreatePaymentView.as_view(), name="create_payment"),
    path("payments/status/<str:session_id>/", PaymentStatusView.as_view(), name="payment_status"),
]
