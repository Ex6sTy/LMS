from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.filters import PaymentFilter
from users.models import CustomUser, Payment
from users.serializers import PaymentSerializer, RegisterSerializer, UserSerializer

from .permissions import IsOwnerOrModer, IsSelf
from .serializers import PrivateUserSerializer, PublicUserSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["date"]
    permission_classes = [IsAuthenticated, IsOwnerOrModer]


class UserProfileAPIView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        elif self.action in ["retrieve", "list"]:
            return [permissions.IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsSelf()]
        return super().get_permissions()


class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return PrivateUserSerializer
        return PublicUserSerializer

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH"):
            return [IsAuthenticated(), IsSelf()]
        return [IsAuthenticated()]
