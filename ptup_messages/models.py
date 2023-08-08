from django.db import models
from accounts.models import User
from django.utils import timezone
from django_quill.fields import QuillField
from django.db.models.aggregates import Count
from random import randint


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sender_messages', null=True,
                               verbose_name='فرستنده ', blank=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='receiver_messages', null=True,
                                 verbose_name='گیرنده ')
    subject = models.CharField(max_length=255, null=True, blank=True, default=None, verbose_name='عنوان')
    # content = models.TextField(verbose_name='متن پیام ')
    content = QuillField()
    is_read = models.BooleanField(verbose_name='خوانده شده/نشده', default=False)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ساخت')

    def __str__(self):
        return f"message {self.id} with sender {self.sender}, receiver {self.receiver}"

    @property
    def get_subject(self):
        return self.subject if self.subject is not None else 'عنوان ندارد'


class MotivationalMessageManger(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class MotivationalMessage(models.Model):
    content = models.TextField()

    objects = MotivationalMessageManger()

    def __str__(self):
        return f"motivational message # {self.id}"


class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sender_notification', null=True,
                               verbose_name='فرستنده ', blank=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='receiver_notification', null=True,
                                 verbose_name='گیرنده ')
    content = models.TextField()