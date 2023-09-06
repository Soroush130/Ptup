from django.urls import path

from followup import views

app_name = 'follow_up'

urlpatterns = [
    path('follow_up_customer/', views.FollowUpCustomer.as_view(), name='follow_up_customer'),
]
