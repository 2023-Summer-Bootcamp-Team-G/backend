from django.urls import path
from .views import Characters

urlpatterns = [
    path('', Characters.as_view()),
    path('<int:character_id>', Characters.as_view()),
]