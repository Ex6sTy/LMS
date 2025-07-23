from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from users.filters import PaymentFilter
from users.models import CustomUser, Payment
from users.serializers import PaymentSerializer, RegisterSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from courses.models import Course
from .permissions import IsOwnerOrModer, IsSelf
from .serializers import PrivateUserSerializer, PublicUserSerializer
from rest_framework.response import Response
from users.services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
)
from users.services import retrieve_stripe_session


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


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Создание оплаты курса",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["course_id"],
            properties={
                "course_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID курса"
                ),
            },
        ),
        responses={200: openapi.Response(description="Ссылка на оплату")},
    )
    def post(self, request):
        course_id = request.data.get("course_id")
        if not course_id:
            return Response({"error": "course_id is required"}, status=400)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Курс не найден"}, status=404)

        amount = course.price

        # Stripe: создаём продукт, цену, сессию
        product_id = create_stripe_product(course.title)
        price_id = create_stripe_price(product_id, amount)
        checkout_url, session_id = create_stripe_session(price_id)

        # Создаём локальный платёж
        Payment.objects.create(
            user=request.user, paid_course=course, amount=amount, method="transfer"
        )

        return Response({"checkout_url": checkout_url, "session_id": session_id})


class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получение статуса оплаты по session_id",
        responses={200: openapi.Response("Статус оплаты")},
    )
    def get(self, request, session_id):
        session = retrieve_stripe_session(session_id)
        return Response(
            {
                "status": session["payment_status"],
                "amount_total": session["amount_total"],
                "currency": session["currency"],
            }
        )
