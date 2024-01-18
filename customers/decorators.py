from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps
from django.utils import timezone
from customers.models import CustomerDiseaseInformation


def pass_foundation_course(view_func):
    """
    این تابع چک میکند آیا بیمار دوره مقدماتی را گذارنده است یا خیر ؟
    :param view_func:
    :return:
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        customer = request.user.customer

        disease_information = CustomerDiseaseInformation.objects.filter(
            customer=customer,
            is_finished=False
        )
        if disease_information.exists():
            if disease_information.first().is_foundation_course:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('customers:foundation_course_customer')
        else:
            messages.info(request, "بیماری برای شما انتخاب نشده است")
            return redirect('home')

    return wrapped_view


def not_pass_healing_period(view_func):
    """
    این تابع بررسی میکند آیا بیمار دوره درمان را گذرانده است یا خیر ؟
    :param view_func:
    :return:
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        customer = request.user.customer

        disease_information = CustomerDiseaseInformation.objects.filter(
            customer=customer,
            is_finished=False
        ).first()

        if not disease_information.is_healing_period:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('follow_up:follow_up_customer')

    return wrapped_view


def has_permission_start_treatment(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        customer = request.user.customer
        if customer.permission_start_treatment:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "شما اجازه شروع درمان را ندارید")
            return redirect('home')

    return wrapped_view
