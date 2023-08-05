"""
URL configuration for gTeamProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from accounts.views import RegisterView, LoginView, LogoutView
from character.views import Characters
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from question.views import Questions

from health.views import health_check

schema_view = get_schema_view(
    openapi.Info(
        title="TeamG API",
        default_version="v1",
        description="Test description",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/questions", Questions.as_view()),
    path("api/characters", Characters.as_view()),
    path("api/characters/", include("character.urls")),
    path("api/register", RegisterView.as_view(), name="register"),
    path("api/login", LoginView.as_view(), name="login"),
    path("api/logout", LogoutView.as_view(), name="logout"),
    path("", include("django_prometheus.urls")),
    path("health", health_check.as_view(), name="health-check"),
]

urlpatterns += [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
