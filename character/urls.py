from django.urls import path
from .views import (
    Characters,
    CharacterDetail,
    nlpAPI,
    DuplicateCharacter,
    KeywordChart,
    Task,
)

urlpatterns = [
    path("", Characters.as_view()),
    path("<int:character_id>", CharacterDetail.as_view()),
    path("api/extract-phrases", nlpAPI.as_view(), name="extract-phrases"),
    path("chart", KeywordChart.as_view()),
    path("duplicate", DuplicateCharacter.as_view()),
    path("<str:task_id>", Task.as_view()),
]
