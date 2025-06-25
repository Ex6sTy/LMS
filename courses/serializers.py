from rest_framework import serializers

from courses.models import Course, Lesson, Subscription
from courses.validators import validate_youtube_link

class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(validators=[validate_youtube_link])
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    video_link = serializers.URLField(validators=[validate_youtube_link])

    class Meta:
        model = Course
        fields = ("id", "name", "description", "preview", "lessons_count", "is_subscribed", "video_link")

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "preview",
            "lessons_count",
            "lessons",
        )

    def get_lessons_count(self, obj):
        return obj.lessons.count()
