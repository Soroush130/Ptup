from django.db.models import QuerySet
from .models import Doctor


def check_information_doctor(user: QuerySet) -> bool:
    """
    این تابع بررسی میکند آیا این کاربری که درخواست داده اطلاعات خودش را تکمیل کرده است
    اگر کامل کرده باشد True برگشت داده می شود
    :param user:
    :return:
    """
    try:
        Doctor.objects.get(user=user)
        return True
    except Doctor.DoesNotExist:
        return False


def check_owner_info(user) -> bool:
    """
    این تابع بررسی می کند ایا کسی که درخواست داده است (request.user) نقش آن دکتر بوده و صاحب این اطلاعات است .
    :param user:
    :return:
    """
    role = user.role
    DOCTOR = 1
    if role == DOCTOR:  # check role user
        if Doctor.objects.get(user=user) == user.doctor:  # check owner info
            return True
        else:
            return False
    else:
        return False
