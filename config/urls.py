from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("/courses/", permanent=False)),
    path("admin/", admin.site.urls),
    path("courses/", include("courses.urls", namespace="courses")),
]
