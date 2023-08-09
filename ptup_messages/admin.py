from django.contrib import admin
from .models import Message, MotivationalMessage, Notification

admin.site.register(Message)

admin.site.register(MotivationalMessage)

admin.site.register(Notification)
