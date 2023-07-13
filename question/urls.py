from django.urls import path
from .views import Question

urlpatterns = [path("", Question.as_view())]
