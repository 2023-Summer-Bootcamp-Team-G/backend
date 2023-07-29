from django.urls import path
from .views import (
    CharacterDetail,
    DuplicateCharacter,
    KeywordChart,
    URLs,
    FinalSubmit,
)


urlpatterns = [
    path("chart", KeywordChart.as_view()),
    path("duplicate", DuplicateCharacter.as_view()),
    path("urls/<str:task_id>", URLs.as_view()),
    path("choice", FinalSubmit.as_view()),
    path("<str:character_id>", CharacterDetail.as_view()),
]
