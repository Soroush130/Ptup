from django.db import models
from accounts.models import User
from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sender_messages', null=True,
                               verbose_name='فرستنده ', blank=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='receiver_messages', null=True,
                                 verbose_name='گیرنده ')
    content = models.TextField(verbose_name='متن پیام ')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ساخت')

    def __str__(self):
        return f"message {self.id} with sender {self.sender}, receiver {self.receiver}"
