from rest_framework.test import APITestCase
from django.urls import reverse
from courses.models import Course, Subscription
from django.contrib.auth import get_user_model

User = get_user_model()

class CourseSubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="1234"
        )
        self.course = Course.objects.create(
            name="Test Course",
            description="Test Desc",
            owner=self.user,
            video_link="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        self.url = reverse("courses:course-list")

    def test_is_subscribed_false(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        print("RESPONSE DATA:", response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_subscribed", response.data["results"][0])
        self.assertFalse(response.data["results"][0]["is_subscribed"])

    def test_is_subscribed_true(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        print("RESPONSE DATA:", response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_subscribed", response.data["results"][0])
        self.assertTrue(response.data["results"][0]["is_subscribed"])

