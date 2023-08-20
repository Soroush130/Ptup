from django.db.models import QuerySet
from django.db import transaction

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
