from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from users.filters import PaymentFilter


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["date"]


class UserProfileAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user