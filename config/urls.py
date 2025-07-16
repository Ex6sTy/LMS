from django.contrib import admin
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import logging
import sys


api_info = openapi.Info(
    title="LMS API",
    default_version="v1",
    description="Документация для проекта LMS",
)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("", lambda request: redirect("/courses/", permanent=False)),
    path("admin/", admin.site.urls),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("courses/", include("courses.urls", namespace="courses")),
    path("swagger.json/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger.yaml/", schema_view.without_ui(cache_timeout=0), name="schema-yaml"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/users/", include("users.urls", namespace="users")),
]
