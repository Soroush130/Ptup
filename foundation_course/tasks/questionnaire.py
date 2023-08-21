from django.db import transaction

from ptup_messages.models import Notification


def get_list_answer_questionnaire(items):
    selected_answers = {}
    for key, value in items:
        if key.startswith('answer'):
            question_id = key[len('answer'):]
            selected_answers[question_id] = value

    return selected_answers


def check_suicide(question_suicide_row: int, questionnaire_answer_id: int, customer):
    from foundation_course.models import QuestionnaireAnswerDetail

    with transaction.atomic():
        receiver = customer.treating_doctor.user

        answer_question = QuestionnaireAnswerDetail.objects.get(
            questionnaire_answer_id=questionnaire_answer_id,
            question__row=question_suicide_row
        )
        if answer_question.question_option.coefficient == 3:
            message = f"بیمار با نام مستعار {customer.nick_name} ریسک خودکشی دارد"
            Notification.objects.create(
                sender=None,
                receiver=receiver,
                content=message
            )
            return True
        else:
            pass
