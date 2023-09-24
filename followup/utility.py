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


def check_question_score(question_id, structure_evaluated, day, customer) -> bool:
    # day = 5
    if day >= 5:
        day_list = list(range(day - 4, day + 1))

        answers = FollowUpQuestionAnswer.objects.filter(question_id=question_id, customer=customer, day__in=day_list)

        if len(answers) == 5:
            if structure_evaluated in ['S', 'A', 'AN', 'TO']:
                scores = [True if answer.score > 7 else False for answer in answers]
                return all(scores)
            elif structure_evaluated in ['H', 'AC', 'GE', 'AT', 'CO', 'NEB']:
                scores = [True if answer.score < 3 else False for answer in answers]
                return all(scores)
        else:
            return False
