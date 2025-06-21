from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Курс", help_text="Укажите курс"
    )
    preview = models.ImageField(
        upload_to="courses/previews",
        null=True,
        blank=True,
        verbose_name="Превью",
        help_text="Загрузите превью",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Введите описание курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        related_name="lessons",
        null=True,
        blank=True,
        help_text="Выберите курс, к которому относится урок",
        verbose_name="Курс",
    )
    name = models.CharField(
        max_length=100, verbose_name="Урок", help_text="Укажите урок"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Введите описание урока",
    )
    photo = models.ImageField(
        upload_to="courses/photo",
        null=True,
        blank=True,
        verbose_name="Фото",
        help_text="Загрузите фото",
    )
    URL = models.URLField(
        blank=True, null=True, verbose_name="Видеоурок", help_text="Загрузите видеоурок"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.name} ({self.course.name})"
