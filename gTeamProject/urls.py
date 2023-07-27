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
from character.views import nlpAPI, Characters
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
<<<<<<< HEAD
from question.views import get_user_data, Questions, get_whoUser_data
=======
from question.views import Questions
>>>>>>> 9c47c1d887fd60beaf88d79e41a2d4a3099f34d0

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
<<<<<<< HEAD
    path("api/user-data", get_user_data, name="get_user_data"),
    path("api/whouser-data", get_whoUser_data, name="get_whoUser_data"),
=======
>>>>>>> 9c47c1d887fd60beaf88d79e41a2d4a3099f34d0
    path("api/questions", Questions.as_view()),
    path("api/characters", Characters.as_view()),
    path("api/characters/", include("character.urls")),
    path("api/register", RegisterView.as_view(), name="register"),
    path("api/login", LoginView.as_view(), name="login"),
    path("api/logout", LogoutView.as_view(), name="logout"),
    path("api/extract-phrases", nlpAPI.as_view(), name="extract-phrases"),
<<<<<<< HEAD
    path("", include("django_prometheus.urls")),
=======
    # path("prometheus/", include("django_prometheus.urls")),
>>>>>>> 9c47c1d887fd60beaf88d79e41a2d4a3099f34d0
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
