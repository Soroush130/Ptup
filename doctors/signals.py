from django.db.models.signals import post_save
from django.dispatch import receiver

from ptup_messages.models import Message
from .models import Doctor


@receiver(post_save, sender=Doctor)
def send_message_after_verify(sender, instance, **kwargs):
    if instance.is_verify:
        return Message.objects.create(
            sender=None,
            receiver=instance.user,
            subject='سامانه ptup',
            content='به سامانه ptup خوش آمدید، اطلاعات شما توسط ادمین سامانه تایید شد'
        )
    else:
        pass
