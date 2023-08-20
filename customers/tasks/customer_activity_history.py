from datetime import datetime

from django.db.models import QuerySet
from django.db.models import Count
from django.db.models.functions import TruncDate

from customers.models import CustomerActivityHistory
from healing_content.models import HealingContent, QuestionnaireWeek


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

def get_questionnaire_weekly(disease_information: QuerySet):
    day = disease_information.day_of_healing_period

    total_number_of_treatment_days = disease_information.healing_period.duration_of_treatment * 7

    list_of_weekend_days = [number for number in range(1, total_number_of_treatment_days) if number % 7 == 0]

    if day in list_of_weekend_days:
        questionnaire_weekly_list = QuestionnaireWeek.objects.filter()
        return questionnaire_weekly_list
    else:
        return None


def get_healing_content(healing_day: QuerySet):
    content_list = HealingContent.objects.filter(healing_day=healing_day)
    return content_list


def get_content_customer(disease_information: QuerySet, healing_day: QuerySet):
    healing_content = get_healing_content(healing_day)
    questionnaires_weekly = get_questionnaire_weekly(disease_information)

    return {
        'healing_content': healing_content,
        'questionnaires_weekly': questionnaires_weekly,
    }
