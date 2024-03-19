
from django.urls import path
from .views import GetQuestion, QuestionAnwser


urlpatterns = [
    
    path('', GetQuestion.as_view(), name = 'tests_home'),
    path('answer/', QuestionAnwser.as_view()),
]
