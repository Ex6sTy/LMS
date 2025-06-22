from django.urls import path
from users.views import (
    PaymentListAPIView,
    UserProfileAPIView,
    RegisterView,
    UserListView,
    UserRetrieveUpdateView,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
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
]
