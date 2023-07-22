from typing import NamedTuple
from collections import namedtuple
from django.db.models import QuerySet

from accounts.utilites import phone_number_decryption
from .models import Doctor


def check_information_doctor(user: QuerySet) -> bool:
    try:
        Doctor.objects.get(user=user)
        return True
    except Doctor.DoesNotExist:
        return False


def get_customer_list_each_doctor(customers: QuerySet) -> NamedTuple:
    customers_list = []
    for customer in customers:
        phone = phone_number_decryption(customer.user.phone)
        Customer = namedtuple("Customer", "id nick_name phone age gender permission_start_treatment")
        customer_new = Customer(customer.id, customer.nick_name, phone, customer.age, customer.gender,
                                customer.permission_start_treatment)
        customers_list.append(customer_new)

    return customers_list
