from datetime import datetime

from django.contrib import messages
from django.db import transaction

from followup.models import FollowUpQuestion, FollowUpQuestionAnswer


def set_start_time_follow_up(disease_information):
    with transaction.atomic():
        start_time_follow_up = disease_information.start_time_follow_up
        if start_time_follow_up is None:
            disease_information.start_time_follow_up = datetime.now()
            disease_information.save()
            return True
        else:
            return False


def check_all_questions_answered(day: int) -> bool:
    count_questions = FollowUpQuestion.objects.all().count()

    answers = FollowUpQuestionAnswer.objects.filter(day=day)

    if answers.count() == count_questions:
        return True
    return False


def increase_follow_up_day(request, disease_information):
    with transaction.atomic():

        status = check_all_questions_answered(day=disease_information.day_of_follow_up)
        if status:
            disease_information.day_of_follow_up += 1
            disease_information.save()
            messages.success(request, "شما به تمام سوالات امروز جواب داده اید")
        else:
            pass
