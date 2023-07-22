from django.urls import path
<<<<<<< HEAD
from .views import Characters, CharacterDetail, DuplicateCharacter, KeywordChart
=======
from .views import (
    Characters,
    CharacterDetail,
    nlpAPI,
    DuplicateCharacter,
    KeywordChart,
    URLs,
    CharacterInfo,
    FinalSubmit,
)
>>>>>>> fbbe7f2ca4704b0d1ed3a16603c1b81a77f583be

urlpatterns = [
    path("", Characters.as_view()),
    path("<int:character_id>", CharacterDetail.as_view()),
    path("chart", KeywordChart.as_view()),
    path("duplicate", DuplicateCharacter.as_view()),
    path("urls/<str:task_id>", URLs.as_view()),
    path("choice", FinalSubmit.as_view()),
    path("info/<str:task_id>", CharacterInfo.as_view()),
]
