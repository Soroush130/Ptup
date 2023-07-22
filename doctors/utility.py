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
