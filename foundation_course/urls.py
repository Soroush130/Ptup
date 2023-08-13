from django.urls import path

from foundation_course import views

app_name = 'foundation_course'

urlpatterns = [
    path('questionnaire/<int:id>/detail/', views.QuestionnaireDetail.as_view(), name='question_detail'),
    path('complete_questionnaire/', views.CompleteQuestionnaireByCustomer.as_view(), name='complete_questionnaire'),
]
