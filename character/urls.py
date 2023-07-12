from django.urls import path
from .views import Characters, CharacterDetail, DuplicateCharacter

urlpatterns = [
    path("", Characters.as_view()),
    path("/<int:character_id>", CharacterDetail.as_view()),
    path("/duplicate", DuplicateCharacter.as_view()),
]
