from django.urls import path
from .views import Questions

urlpatterns = [path("", Questions.as_view())]
