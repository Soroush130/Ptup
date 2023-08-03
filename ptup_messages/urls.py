from django.urls import path
from . import views

app_name = "ptup_messages"

urlpatterns = [
    path("messages/", views.MessagesView.as_view(), name='messages'),
    path("messages/detail/<int:message_id>/", views.DetailMessageView.as_view(), name='messages-detail'),
    path("messages/delete/<int:message_id>/", views.DeleteMessageView.as_view(), name='messages-delete'),
]
