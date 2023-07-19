from django.db import models
from accounts.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sender_messages', null=True,
                               verbose_name='فرستنده ')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='receiver_messages', null=True,
                                 verbose_name='گیرنده ')
    content = models.TextField(verbose_name='متن پیام ')

    def __str__(self):
        return f"message {self.id} with sender {self.sender}, receiver {self.receiver}"
