from django.urls import path
from . import views

app_name = 'system_guide'

urlpatterns = [
    path('guide/', views.GuidePageView.as_view(), name='guide')
]