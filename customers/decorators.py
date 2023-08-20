from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

from django.utils import timezone

from customers.models import CustomerDiseaseInformation
from healing_content.models import PracticeAnswer


def pass_foundation_course(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        customer = request.user.customer

        disease_information = CustomerDiseaseInformation.objects.filter(
            customer=customer,
            is_finished=False
        ).first()

        if disease_information.is_foundation_course:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('customers:foundation_course_customer')

    return wrapped_view


def check_practice_answer(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        customer = request.user.customer

        date_now = timezone.now().date()
        practice_answer = PracticeAnswer.objects.filter(
            customer=customer,
            time_answer__year=date_now.year,
            time_answer__month=date_now.month,
            time_answer__day=date_now.day
        )

        if not practice_answer.exists():
            return view_func(request, *args, **kwargs)
        else:
            messages.info(request, 'شما تمرینات امروز را انجام داده اید')
            return redirect('customers:healing_period')

    return wrapped_view


def has_started_healing_period(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        customer = request.user.customer

        disease_information = CustomerDiseaseInformation.objects.filter(
            customer=customer,
            is_finished=False
        ).first()

        if disease_information.start_time_period is None:
            messages.info(request, "شما هنوز دوره درمان را شروع نکردید")
            return redirect('customers:healing_period')
        else:
            return view_func(request, *args, **kwargs)

    return wrapped_view
