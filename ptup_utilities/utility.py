from typing import Any

from django.db.models import QuerySet

from customers.models import Customer, CustomerDiseaseInformation
from ptup_messages.models import Message, MotivationalMessage, Notification


def get_context_customer(user: QuerySet) -> dict:
    motivational_message = MotivationalMessage.objects.random()
    context = {
        "motivational_message": motivational_message,
    }
    return context


# ===================================================================================

def get_list_customers_in_foundation_course(doctor):
    list_customers_in_foundation_course = CustomerDiseaseInformation.objects.filter(
        customer__treating_doctor=doctor,
        is_finished=False,
        is_foundation_course=False,
        is_healing_period=False,
        is_follow_up=False
    )
    return list_customers_in_foundation_course


def get_list_customers_in_healing_period(doctor):
    list_customers_in_healing_period = CustomerDiseaseInformation.objects.filter(
        customer__treating_doctor=doctor,
        is_finished=False,
        is_foundation_course=True,
        is_healing_period=False,
        is_follow_up=False
    )
    return list_customers_in_healing_period


def get_list_customers_in_follow_up(doctor):
    list_customers_in_follow_up = CustomerDiseaseInformation.objects.filter(
        customer__treating_doctor=doctor,
        is_finished=False,
        is_foundation_course=True,
        is_healing_period=True,
        is_follow_up=False
    )
    return list_customers_in_follow_up


def get_context_doctor(user: QuerySet) -> dict:
    doctor = user.doctor
    if doctor.is_verify:
        list_customers = Customer.objects.filter(treating_doctor=doctor)
        count_customers = list_customers.count()

        list_messages_not_read = Message.objects.filter(receiver=user, is_read=False)
        count_messages_not_read = list_messages_not_read.count()

        list_customers_in_foundation_course = get_list_customers_in_foundation_course(doctor)

        list_customers_in_healing_period = get_list_customers_in_healing_period(doctor)

        list_customers_in_follow_up = get_list_customers_in_follow_up(doctor)

        context = {
            "count_customers": count_customers,
            "count_messages_not_read": count_messages_not_read,

            "list_customers_in_foundation_course": list_customers_in_foundation_course,
            "list_customers_in_healing_period": list_customers_in_healing_period,
            "list_customers_in_follow_up": list_customers_in_follow_up,
        }
        return context
    else:
        return {}


# ===================================================================================

def get_context_according_user_role(user: QuerySet, user_role: int) -> dict:
    DOCTOR = 1
    context = get_context_doctor(user) if user_role == DOCTOR else get_context_customer(user)

    return context


def send_message_in_protable(receiver: QuerySet, content: str, sender: QuerySet) -> bool:
    Notification.objects.create(receiver=receiver, content=content, sender=sender)
    return True


# ====================== Session Django ======================
def set_session(request, key: str, value: Any) -> None:
    request.session[key] = value
    request.session.save()


def get_session(request, key: str) -> str:
    if request.session.has_key(key):
        value = request.session[key]
        return value
    else:
        pass


def delete_session(request, key: str) -> None:
    if request.session.has_key(key):
        del request.session[key]
    else:
        pass
