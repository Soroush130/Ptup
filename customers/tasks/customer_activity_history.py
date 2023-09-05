from datetime import datetime

from django.db.models import QuerySet
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta

from django.utils import timezone

from customers.models import CustomerActivityHistory
from healing_content.models import HealingContent, QuestionnaireWeek, HealingWeek, QuestionnaireWeekAnswer, Practice, \
    QuestionPractice, AnswerPractice


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
def check_exercises_every_week(week, disease_information, healing_period, customer):

    if week > 0:

        healing_week = HealingWeek.objects.get(week=week, healing_period=healing_period)

        questionnaires_weekly, questionnaires_weekly_count = get_questionnaire_weekly(disease_information,
                                                                                      healing_period.duration_of_treatment)

        if questionnaires_weekly is not None:
            questionnaire_answer_weekly = QuestionnaireWeekAnswer.objects.filter(
                questionnaire_week__in=questionnaires_weekly, healing_week=healing_week)

            if (questionnaire_answer_weekly.exists()) and (
                    questionnaire_answer_weekly.count() == questionnaires_weekly_count):
                status_questionnaire_answer_weekly = True
            else:
                status_questionnaire_answer_weekly = False

        else:
            status_questionnaire_answer_weekly = None

        status_practice_answer = AnswerPractice.objects.filter(healing_week=healing_week.id, customer=customer).exists()

        if status_questionnaire_answer_weekly in [0, 1]:  # status_questionnaire_answer_weekly == True or False

            if status_practice_answer and status_questionnaire_answer_weekly:
                return True, week + 1, healing_period
            return False, week, healing_period

        else:  # status_questionnaire_answer_weekly == None
            if status_practice_answer:
                return True, week + 1, healing_period
            return False, week, healing_period
    else:
        return True, week + 1, healing_period


def get_questionnaire_weekly(disease_information, duration_of_treatment):
    date_now = timezone.now()

    start_time_period = disease_information.start_time_period

    total_number_of_treatment_days = duration_of_treatment * 7

    list_of_weekend_days: list[int] = [number for number in range(1, total_number_of_treatment_days) if number % 7 == 0]

    list_of_weekend_dates: list[datetime] = []
    for day in list_of_weekend_days:
        date = start_time_period.date() + timedelta(days=day)
        list_of_weekend_dates.append(date)

    # date_now = datetime.strptime("2023-09-06", "%Y-%m-%d").date()

    if date_now in list_of_weekend_dates:
        questionnaire_weekly_list = QuestionnaireWeek.objects.all()
        return questionnaire_weekly_list, questionnaire_weekly_list.count()
    else:
        return None, 0


def get_healing_content(healing_week: QuerySet):
    content_list = HealingContent.objects.filter(healing_week=healing_week)
    return content_list


def get_practices_healing_week(healing_week):
    practices_dict = {}
    practices = Practice.objects.filter(healing_week=healing_week)
    for practice in practices:
        # answer_practice = AnswerPractice.objects.filter(healing_week=healing_week, question_practice__practice=practice)

        questions = QuestionPractice.objects.filter(practice=practice)

        # if questions.count() != answer_practice.count():
        practices_dict[practice] = list(questions)

    return practices_dict


def get_content_customer(disease_information: QuerySet, week: int, duration_of_treatment: int, healing_week: QuerySet):
    healing_content = get_healing_content(healing_week)
    practices_dict = get_practices_healing_week(healing_week)
    questionnaires_weekly, questionnaires_weekly_count = get_questionnaire_weekly(
        disease_information=disease_information,
        duration_of_treatment=duration_of_treatment
    )

    return {
        'healing_content': healing_content,
        'practices_dict': practices_dict,
        'questionnaires_weekly': questionnaires_weekly,
    }
