from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps
from .utility import check_information_doctor
from customers.utility import check_information_customer


def is_complete_information_doctor(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        DOCTOR, CUSTOMER = 1, 2
        user_role = request.user.role
        if user_role == DOCTOR:
            status = check_information_doctor(request.user)
            if status:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "ابتدا اطلاعات خود را تکمیل کنید")
                return redirect('doctors:completion_information_doctor')

        return view_func(request, *args, **kwargs)

    return wrapped_view


def is_complete_information(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        DOCTOR, CUSTOMER = 1, 2
        user_role = request.user.role
        if user_role == DOCTOR:
            status = check_information_doctor(request.user)
            if status:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "ابتدا اطلاعات خود را تکمیل کنید")
                return redirect('doctors:completion_information_doctor')
        elif user_role == CUSTOMER:
            status = check_information_customer(request.user)
            if status:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "ابتدا اطلاعات خود را تکمیل کنید")
                return redirect('customers:completion_information_customer')
        else:
            return HttpResponse("شما ادیمن سایت هستید")

        # return view_func(request, *args, **kwargs)

    return wrapped_view
