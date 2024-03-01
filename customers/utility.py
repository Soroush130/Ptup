from django.db.models import QuerySet

from customers.models import Customer


def normalize_data_filter_customer(customers: QuerySet) -> dict:
    """
        This function used to convert data queryset to json
    :param customers:
    :return:
    """
    customers_dict = {}
    for customer in customers:
        customers_dict[customer.id] = {
            "id": customer.id,
            "phone": customer.phone,
            "nick_name": customer.nick_name,
            "age": customer.age,
            "gender": customer.gender,
            "permission_start_treatment": customer.permission_start_treatment,
        }
    return customers_dict


def check_information_customer(user: QuerySet) -> bool:
    """
    این تابع بررسی میکند آیا این کاربری که درخواست داده اطلاعات خودش را تکمیل کرده است
    اگر کامل کرده باشد True برگشت داده می شود
    :param user:
    :return:
    """
    try:
        Customer.objects.get(user=user)
        return True
    except Customer.DoesNotExist:
        return False
