from django.db.models import QuerySet

from customers.models import Customer
from ptup_messages.models import Message


def get_context_customer(user: QuerySet) -> dict:
    context = {}
    return context


def get_context_doctor(user: QuerySet) -> dict:
    list_customers = Customer.objects.filter(treating_doctor=user.doctor)
    count_customers = list_customers.count()

    list_messages_not_read = Message.objects.filter(receiver=user, is_read=False)
    count_messages_not_read = list_messages_not_read.count()

    context = {
        "count_customers": count_customers,
        "count_messages_not_read": count_messages_not_read,
    }
    return context


def get_context_according_user_role(user: QuerySet, user_role: int) -> dict:
    DOCTOR = 1
    context = get_context_doctor(user) if user_role == DOCTOR else get_context_customer(user)

    return context


def send_message_in_protable(receiver: QuerySet, content: str, sender: QuerySet = None):
    content = f"{receiver} {content}"
    Message.objects.create(receiver=receiver.user, content=content)
    return True
