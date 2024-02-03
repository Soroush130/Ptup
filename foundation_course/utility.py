from django.db.models import QuerySet
from foundation_course.models import Question


def calculate_score_each_questionnaire(questionnaire_answer, answers: list) -> float:
    """
        This function used to calculation score each questionnaire
    :param questionnaire_answer:
    :param answers:
    :return:
    """

    score = 0
    for answer in answers:
        score += answer.question_option.coefficient

    questionnaire_answer.score = score
    questionnaire_answer.save()
    return score


def calculate_score_each_questionnaire_weekly(questionnaire_answer, answers: list) -> float:
    """
        This function used to calculation score each questionnaire weekly
    :param questionnaire_answer:
    :param answers:
    :return:
    """

    score = 0
    for answer in answers:
        score += answer.question_option_week.coefficient

    questionnaire_answer.score = score
    questionnaire_answer.save()
    return score


def check_question_for_questionnaire(questionnaire: QuerySet):
    """
    Check the existence of a question for the preliminary questionnaire
    :return:
    """
    questions = Question.objects.filter(questionnaire=questionnaire).order_by('row')
    if questions.exists():
        return True, questions
    else:
        return False, None
