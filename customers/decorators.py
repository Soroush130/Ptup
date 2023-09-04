from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps
from datetime import timedelta
from django.utils import timezone

from customers.models import CustomerDiseaseInformation
from customers.tasks.customer_activity_history import get_questionnaire_weekly, check_exercises_every_week
from healing_content.models import HealingWeek, QuestionnaireWeekAnswer, AnswerPractice, Practice, QuestionPractice


def pass_foundation_course(view_func):
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


def pass_healing_period(view_func):
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
            return redirect('customers:follow_up_customer')

    return wrapped_view

#
# def check_practice_answer(view_func):
#     @wraps(view_func)
#     def wrapped_view(request, *args, **kwargs):
#         customer = request.user.customer
#         disease_information = CustomerDiseaseInformation.objects.filter(
#             customer=customer,
#             is_finished=False
#         ).first()
#         week = disease_information.day_of_healing_period
#         healing_period = disease_information.healing_period
#
#         # TODO: Checking whether she passed the previous week's training or not
#         status, week, healing_period = check_exercises_every_week(
#             week - 1,
#             disease_information,
#             healing_period,
#             customer
#         )
#
#         if status:
#             return view_func(request, *args, **kwargs)
#
#     return wrapped_view


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
