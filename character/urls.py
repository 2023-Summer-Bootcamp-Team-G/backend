from django.urls import path
from .views import Characters, CharacterDetail, nlpAPI

urlpatterns = [
    path("", Characters.as_view()),
    path("<int:character_id>", CharacterDetail.as_view()),
    path("api/extract-phrases", nlpAPI.as_view(), name="extract-phrases"),
]
