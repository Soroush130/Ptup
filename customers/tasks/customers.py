from django.contrib import messages
from django.db.models import QuerySet
from django.db import transaction
from django.utils import timezone
from customers.models import CustomerDiseaseInformation
# from customers.tasks.customer_activity_history import get_practices_healing_week
from healing_content.models import HealingWeek, QuestionnaireWeekAnswer, AnswerPractice, Practice, QuestionPractice, \
    QuestionnaireWeek, HealingWeekViewLog


def create_healing_content_view_log(user, healing_week):
    instance, created = HealingWeekViewLog.objects.get_or_create(user=user, healing_week=healing_week)
    return instance, created

def increase_week_of_healing_period(request, customer: QuerySet):
    """
    This is function used to increase week of healing period when register practice answer
    :param customer:
    :return:
    """
    with transaction.atomic():
        disease_information = CustomerDiseaseInformation.objects.filter(
            customer=customer,
            is_finished=False
        ).first()

        healing_period = disease_information.healing_period
        week = disease_information.week_of_healing_period

        healing_week = HealingWeek.objects.get(week=week, healing_period=healing_period)
        practices = Practice.objects.filter(healing_week=healing_week)
        # questions_in_practice = QuestionPractice.objects.filter(practice__in=practices)
        answers_in_practices = AnswerPractice.objects.filter(practice__in=practices,
                                                             customer=customer)

        if answers_in_practices.exists():

            if answers_in_practices.count() == practices.count():

                # Register healing content view log for user
                create_healing_content_view_log(user=request.user, healing_week=healing_week)
                disease_information.week_of_healing_period += 1
                disease_information.save()
                messages.success(request, "به هفته درمانی جدید خوش آمدید")


            else:
                messages.error(request, "لطفا به باقی تمرین ها جواب بدهید")


def set_time_healing_period(customer_information: QuerySet) -> bool:
    """
    This is function used to set time start healing period
    :param customer_information:
    :return:
    """
    with transaction.atomic():
        if customer_information.start_time_period is None:
            customer_information.start_time_period = timezone.now()
            customer_information.save()
            return True
        else:
            return False


def get_practice_answer_list(customer: QuerySet):
    answers_list = []

    customer_info = CustomerDiseaseInformation.objects.filter(
        customer=customer,
        is_finished=False
    ).first()

    duration_of_treatment = customer_info.healing_period.duration_of_treatment

    for week in range(1, duration_of_treatment + 1):

        healing_week = HealingWeek.objects.filter(week=week, healing_period=customer_info.healing_period)

        if healing_week.exists():
            practice_answer = AnswerPractice.objects.filter(customer=customer, healing_week=healing_week.first().id)

            if practice_answer.exists():
                practice_answer_id = practice_answer.first().id
                answers_list.append({
                    'practice_answer_id': practice_answer_id,
                    'healing_week': healing_week.first(),
                    'week': week,
                    'status': True
                })
            else:
                answers_list.append({
                    'practice_answer_id': None,
                    'healing_week': healing_week.first(),
                    'week': week,
                    'status': False
                })
        else:
            answers_list.append({
                'practice_answer_id': None,
                'healing_week': healing_week.first(),
                'week': week,
                'status': False
            })

    return answers_list


def check_last_day_healing_period(request, healing_day_id, customer):
    with transaction.atomic():
        healing_week = HealingWeek.objects.get(id=healing_day_id)

        healing_period_last_day = healing_week.healing_period.duration_of_treatment
        # healing_period_last_day = 2

        if healing_week.week == healing_period_last_day:
            disease_info = CustomerDiseaseInformation.objects.filter(customer=customer, is_finished=False).first()
            disease_info.is_healing_period = True
            disease_info.save()
            messages.success(request, "شما دوره درمانی را با موفقیت سپری کردید")
        else:
            pass


def get_progress_charts(customer: QuerySet):
    questionnaire_weekly_list = []
    questionnaire_weekly_answer_list = QuestionnaireWeekAnswer.objects.filter(customer=customer)

    for questionnaire in questionnaire_weekly_answer_list:
        questionnaire_week = questionnaire.questionnaire_week
        if questionnaire_week not in questionnaire_weekly_list:
            questionnaire_weekly_list.append(questionnaire_week)
        else:
            pass

    charts = []
    for questionnaire_weekly in questionnaire_weekly_list:
        questionnaire_answer = QuestionnaireWeekAnswer.objects.filter(customer=customer,
                                                                      questionnaire_week=questionnaire_weekly)

        labels = []
        data = []
        for index, item in enumerate(questionnaire_answer.order_by('answer_time')):
            labels.append(f"هفته {index + 1}")
            data.append(item.score)

        charts.append({
            "questionnaire_week_id": questionnaire_weekly.id,
            "questionnaire_week_title": questionnaire_weekly.title,
            "labels": labels,
            "data": data
        })

    return charts

#################################################################
# def group_by_healing_content_each_week(healing_week) -> dict:
#     group_by_contents = {}
#     for day in range(1, 8):
#         contents_in_day = HealingContent.objects.filter(healing_week=healing_week, day=day)
#         group_by_contents[day] = list(contents_in_day)
#
#     return group_by_contents
