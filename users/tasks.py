from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser


@shared_task
def send_course_update_email(user_email, course_title):
    send_mail(
        subject=f"Обновление курса: {course_title}",
        message=f"Привет! Курс «{course_title}» был обновлён. Загляни скорее!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )


@shared_task
def deactivate_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    users = CustomUser.objects.filter(is_active=True, last_login__lt=one_month_ago)
    count = users.update(is_active=False)
    return f"Deactivated {count} users"