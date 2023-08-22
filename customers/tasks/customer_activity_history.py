from datetime import datetime

from django.db.models import QuerySet
from django.db.models import Count
from django.db.models.functions import TruncDate

from customers.models import CustomerActivityHistory
from healing_content.models import HealingContent, QuestionnaireWeek, HealingDay, PracticeAnswer, \
    QuestionnaireWeekAnswer


def create_activity_history(customer_id, subject, content) -> QuerySet:
    new_activity = CustomerActivityHistory.objects.create(
        customer_id=customer_id,
        subject=subject,
        content=content
    )

    return new_activity


def get_activity_list(customer: QuerySet) -> dict:
    timeline = {}

    grouped_data = CustomerActivityHistory.objects.filter(
        customer=customer
    ).annotate(
        created_date=TruncDate('created')  # Truncate datetime to date
    ).values('created_date').annotate(
        activity_count=Count('id')
    ).order_by('created_date')

    for date in grouped_data:
        year, month, day = date['created_date'].year, date['created_date'].month, date['created_date'].day
        activities = get_activity(year, month, day, customer)

        timeline[date['created_date'].strftime('%Y-%m-%d')] = list(activities)

    return timeline


def get_activity(year, month, day, customer: QuerySet):
    return CustomerActivityHistory.objects.filter(
        customer=customer,
        created__year=year,
        created__month=month,
        created__day=day
    ).order_by('-created')


# ===================================== Healing Content Customer =========================
def check_exercises_every_day(day, healing_period, customer):
    """
    در این تابع ما چک می کنیم که آیا این کاربر تمرینات یا اگر پرسشنامه ای در آن روز یا روز قبل خود دارد تکمیل کرده است یا خیر
    :param day:
    :param healing_period:
    :param customer:
    :return:
    """
    if day > 0:

        healing_day = HealingDay.objects.get(day=day, healing_period=healing_period)

        questionnaires_weekly = get_questionnaire_weekly(day, healing_period.duration_of_treatment)

        if questionnaires_weekly is not None:
            status_questionnaire_answer_weekly = QuestionnaireWeekAnswer.objects.filter(
                questionnaire_week__in=questionnaires_weekly).exists()
        else:
            status_questionnaire_answer_weekly = None

        status_practice_answer = PracticeAnswer.objects.filter(healing_day=healing_day.id, customer=customer).exists()

        if status_questionnaire_answer_weekly in [0, 1]:  # status_questionnaire_answer_weekly == True or False

            if status_practice_answer and status_questionnaire_answer_weekly:
                return True, day + 1, healing_period
            return False, day, healing_period

        else:  # status_questionnaire_answer_weekly == None
            if status_practice_answer:
                return True, day + 1, healing_period
            return False, day, healing_period
    else:
        return True, day + 1, healing_period


def get_questionnaire_weekly(day, duration_of_treatment):
    total_number_of_treatment_days = duration_of_treatment * 7

    list_of_weekend_days = [number for number in range(1, total_number_of_treatment_days) if number % 7 == 0]
    # list_of_weekend_days = [1]

    if day in list_of_weekend_days:
        questionnaire_weekly_list = QuestionnaireWeek.objects.all()
        return questionnaire_weekly_list
    else:
        return None


def get_healing_content(healing_day: QuerySet):
    content_list = HealingContent.objects.filter(healing_day=healing_day)
    return content_list


def get_content_customer(day: int, duration_of_treatment: int, healing_day: QuerySet):
    healing_content = get_healing_content(healing_day)
    questionnaires_weekly = get_questionnaire_weekly(day, duration_of_treatment)

    return {
        'healing_content': healing_content,
        'questionnaires_weekly': questionnaires_weekly,
    }
