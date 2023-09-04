from django.urls import path

from . import views

app_name = "healing_content"

urlpatterns = [
    path('day_feedback_detail/<int:customer_id>/<int:healing_week_id>/', views.DayFeedbackView.as_view(),
         name="day_feedback_detail"),

    # path('show_feedback/<int:healing_week_id>/', views.ShowFeedbackByCustomerView.as_view(), name="show_feedback"),

    path('create_feedback/', views.CreateFeedbackView.as_view(), name="create_feedback"),

    # Questionnaire Weekly
    path('questionnaire_weekly/<int:questionnaire_id>/<int:healing_week_id>/', views.QuestionnaireWeeklyView.as_view(),
         name="questionnaire_weekly"),

    path('complate_questionnaire_weekly/', views.CompleteQuestionnaireWeeklyByCustomer.as_view(),
         name="complate_questionnaire_weekly"),
]
