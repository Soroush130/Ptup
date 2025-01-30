from django.urls import path
from . import views

app_name = 'question_answer'

urlpatterns = [
    path('question/', views.QuestionView.as_view(), name='question'),
    path('question_detail/<int:question_id>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('answer/', views.AnswerView.as_view(), name='answer'),
    path('submit_answer/<int:question_id>/', views.SubmitAnswerView.as_view(), name='submit_answer'),
    path('submit_question/', views.SubmitQuestionView.as_view(), name='submit_question'),
]