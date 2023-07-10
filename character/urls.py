from django.urls import path
from .views import Characters, CharacterDetail

urlpatterns = [
    path('', Characters.as_view()),
    path('/<int:character_id>', CharacterDetail.as_view()),
]