from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps
from datetime import timedelta
from django.utils import timezone

from customers.models import CustomerDiseaseInformation
from customers.tasks.customer_activity_history import get_questionnaire_weekly
from healing_content.models import HealingDay, QuestionnaireWeekAnswer, AnswerPractice


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


def check_practice_answer(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        customer = request.user.customer

        date_now = timezone.now().date()

        practice_answers = AnswerPractice.objects.filter(customer=customer)

        if practice_answers.exists():
            last_practice_answer = AnswerPractice.objects.filter(customer=customer).last()
            if (last_practice_answer.time_answer.year == date_now.year) and (
                    last_practice_answer.time_answer.month == date_now.month) and (
                    last_practice_answer.time_answer.day == date_now.day):

                healing_day = HealingDay.objects.get(id=last_practice_answer.healing_day.id)

                questionnaires_weekly, questionnaires_weekly_count = get_questionnaire_weekly(
                    healing_day.day,
                    healing_day.healing_period.duration_of_treatment
                )

                if questionnaires_weekly is not None:
                    questionnaire_answer_weekly = QuestionnaireWeekAnswer.objects.filter(
                        questionnaire_week__in=questionnaires_weekly)

                    if (questionnaire_answer_weekly.exists()) and (
                            questionnaire_answer_weekly.count() == questionnaires_weekly_count):
                        messages.info(request, 'شما تمرینات امروز را انجام داده اید')
                        return redirect('customers:healing_period')
                    else:
                        messages.error(request, "پرسشنامه های هقتگی را تکمیل کنید")
                        return view_func(request, *args, **kwargs)
                else:
                    messages.info(request, 'شما تمرینات امروز را انجام داده اید')
                    return redirect('customers:healing_period')
            else:
                messages.error(request, "لطفا تمرین امروز را انجام بدهید")
                return view_func(request, *args, **kwargs)
        else:
            # messages.info(request, "به اولین روز از دوره درمان خوش آمدید")
            return view_func(request, *args, **kwargs)

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
