from django.db.models import QuerySet

from ptup_messages.models import Message


def get_context_according_user_role(user: QuerySet) -> dict:
    context = {}

    return context


def send_message_in_protable(receiver: QuerySet, content: str, sender: QuerySet = None):
    content = f"{receiver} {content}"
    Message.objects.create(receiver=receiver.user, content=content)
    return True
