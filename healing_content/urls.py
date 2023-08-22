from django.urls import path

from . import views

app_name = "healing_content"

urlpatterns = [
    path('day_feedback_detail/<int:practice_answer_id>/', views.DayFeedbackView.as_view(), name="day_feedback_detail"),
    path('create_feedback/', views.CreateFeedbackView.as_view(), name="create_feedback"),
]