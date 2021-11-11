from django.urls import path
from .views import *

urlpatterns = [
    path('departments', DepartmentList.as_view(), name="departments"),
    path('users', UserCreate.as_view(), name="users"),
    path('users/<int:pk>', UserRetrieveUpdateDestory.as_view(), name="user"),
    path('questions', QuestionListCreate.as_view(), name="questions"),
    path('questions/<int:pk>', QuestionRetrieveUpdateDestroy.as_view(),
         name="question"),
    path('questions/<int:pk>/answers',
         AnswerListCreate.as_view(), name="question-answers"),
    path('questions/<int:pk>/answers/<int:val>',
         AnswerRetrieveUpdateDestroy.as_view(), name="question-answer"),
    path('questions/<int:pk>/vote', vote_question, name="question-vote"),
    path('answers/<int:pk>/vote', vote_answer, name="answer-vote"),
    path('questions/<int:pk>/flag',
         QuestionFlagsCreate.as_view(), name="question-flag"),
    path('answers/<int:pk>/flag', AnswerFlagsCreate.as_view(), name="answer-flag"),
]
