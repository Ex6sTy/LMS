from django_filters import rest_framework as filters
from users.models import Payment


class PaymentFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=[("date", "date")],
        field_labels={"date": "Дата оплаты"},
    )
    paid_course = filters.NumberFilter(field_name="paid_course__id", label="Курс")
    paid_lesson = filters.NumberFilter(field_name="paid_lesson__id", label="Урок")
    method = filters.ChoiceFilter(choices=Payment.PaymentMethod.choices)

    class Meta:
        model = Payment
        fields = ["paid_course", "paid_lesson", "method"]
