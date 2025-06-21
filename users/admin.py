from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "method", "date", "paid_course", "paid_lesson")
    list_filter = ("method", "date")
    search_fields = ("user__email",)


