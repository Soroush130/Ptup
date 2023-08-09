from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

from customers.models import CustomerDiseaseInformation


def pass_foundation_course(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        customer = request.user.customer

        disease_information = CustomerDiseaseInformation.objects.get(customer=customer)

        if disease_information.is_foundation_course:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('customers:foundation_course_customer')

    return wrapped_view



