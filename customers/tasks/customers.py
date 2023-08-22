from django.db.models import QuerySet
from django.db import transaction
from django.utils import timezone

from customers.models import CustomerDiseaseInformation
from customers.tasks.customer_activity_history import check_exercises_every_day
from healing_content.models import PracticeAnswer, HealingDay


def increase_day_of_healing_period(customer: QuerySet) -> bool:
    """
    This is function used to increase day of healing period when register practice answer
    :param customer:
    :return:
    """
    with transaction.atomic():
        diseas_customer = CustomerDiseaseInformation.objects.filter(
            customer=customer,
            is_finished=False
        ).first()

        healing_period = diseas_customer.healing_period
        day = diseas_customer.day_of_healing_period

        status, day, healing_period = check_exercises_every_day(day, healing_period, customer)
        if status:
            diseas_customer.day_of_healing_period += 1
            diseas_customer.save()
            return True
        else:
            return False


def set_time_healing_period(customer_information: QuerySet) -> bool:
    """
    This is function used to set time start healing period
    :param customer_information:
    :return:
    """
    with transaction.atomic():
        if customer_information.start_time_period is None:
            customer_information.start_time_period = timezone.now()
            customer_information.save()
            return True
        else:
            return False


def get_practice_answer_list(customer: QuerySet):
    answers_list = []

    customer_info = CustomerDiseaseInformation.objects.filter(
        customer=customer,
        is_finished=False
    ).first()

    duration_of_treatment = customer_info.healing_period.duration_of_treatment * 7

    for day in range(1, duration_of_treatment + 1):

        healing_day = HealingDay.objects.filter(day=day, healing_period=customer_info.healing_period)

        if healing_day.exists():
            practice_answer = PracticeAnswer.objects.filter(customer=customer, healing_day=healing_day.first().id)
            if practice_answer.exists():
                practice_answer_id = practice_answer.first().id
                answers_list.append({
                    'practice_answer_id': practice_answer_id,
                    'day': day,
                    'status': True
                })
            else:
                answers_list.append({
                    'practice_answer_id': None,
                    'day': day,
                    'status': False
                })
        else:
            answers_list.append({
                'practice_answer_id': None,
                'day': day,
                'status': False
            })

    return answers_list


def check_last_day_healing_period(healing_day_id, customer):
    with transaction.atomic():
        healing_day = HealingDay.objects.get(id=healing_day_id)
        healing_period_last_day = healing_day.healing_period.duration_of_treatment * 7
        if healing_day.day == healing_period_last_day:
            disease_info = CustomerDiseaseInformation.objects.filter(customer=customer, is_finished=False).first()
            disease_info.is_healing_period = True
            disease_info.save()
        else:
            pass
