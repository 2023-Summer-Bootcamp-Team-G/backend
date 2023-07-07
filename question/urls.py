from django.contrib import admin
from django.urls import path
from .views import question

urlpatterns = [
    path('', question)
]