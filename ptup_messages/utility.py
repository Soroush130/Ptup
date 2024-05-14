from django.db.models import QuerySet

from customers.models import Customer


def read_message(message: QuerySet) -> bool:
    try:
        message.is_read = True
        message.save()
        return True
    except:
        return False


def get_contacts_doctor(user):
    doctor = user.doctor
    customers = Customer.objects.filter(treating_doctor=doctor)
    return customers


def get_contacts_customer(user):
    customer = Customer.objects.get(user=user)
    return customer.treating_doctor
