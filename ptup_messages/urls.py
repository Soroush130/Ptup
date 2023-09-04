from django.urls import path
from . import views

app_name = "ptup_messages"

urlpatterns = [
    path("messages/", views.MessagesView.as_view(), name='messages'),
    path("send_messages/", views.SendMessageView.as_view(), name='send_messages'),
    path("messages/detail/<int:message_id>/", views.DetailMessageView.as_view(), name='messages-detail'),
    path("messages/delete/<int:message_id>/", views.DeleteMessageView.as_view(), name='messages-delete'),

    # Notification
    path("notifications/", views.NotificationView.as_view(), name='notifications'),
]
