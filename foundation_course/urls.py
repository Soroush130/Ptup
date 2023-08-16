from django.urls import path, include

from foundation_course import views

app_name = 'foundation_course'

urlpatterns = [
    path('api/', include('foundation_course.api.urls')),

    path('questionnaire/<int:id>/detail/', views.QuestionnaireDetail.as_view(), name='question_detail'),
    path('complete_questionnaire/', views.CompleteQuestionnaireByCustomer.as_view(), name='complete_questionnaire'),
]
