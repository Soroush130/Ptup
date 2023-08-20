from django.db.models import QuerySet
from django.db import transaction
from django.utils import timezone

from customers.models import CustomerDiseaseInformation


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
        diseas_customer.day_of_healing_period += 1
        diseas_customer.save()
        return True


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