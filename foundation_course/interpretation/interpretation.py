def interpretation_bai(score: float) -> str:
    if score <= 7:
        return 'اضطراب کم'
    elif 8 <= score <= 15:
        return 'اضطراب خفیف'
    elif 16 <= score <= 25:
        return 'اضطراب متوسط'
    else:
        return 'اضطراب شدید'


def interpretation_bdi(score: float) -> str:
    if score <= 13:
        return 'افسردگی کم'
    elif 14 <= score <= 19:
        return 'افسردگی خفیف'
    elif 20 <= score <= 28:
        return 'افسردگی متوسط'
    else:
        return 'افسردگی شدید'


# ========================================== DERS =================================
def interpretation_ders(score: float, id: int) -> dict:
    from foundation_course.models import QuestionnaireAnswerDetail
    answer_list = QuestionnaireAnswerDetail.objects.filter(questionnaire_answer_id=id)
    result_clarity = index_clarity(answer_list)
    result_aware = index_aware(answer_list)
    result_impulse = index_impulse(answer_list)
    result_nonaccept = index_nonaccept(answer_list)
    result_strategies = index_strategies(answer_list)
    result_goals = index_goals(answer_list)
    return {
        'clarity': {
            'score_clarity': result_clarity,
            'small_unit': "5",
            'large_unit': "25"
        },
        'aware': {
            'score_aware': result_aware,
            'small_unit': "6",
            'large_unit': "30"
        },
        'impulse': {
            'score_impulse': result_impulse,
            'small_unit': "6",
            'large_unit': "30"
        },
        'nonaccept': {
            'score_nonaccept': result_nonaccept,
            'small_unit': "6",
            'large_unit': "30"
        },
        'strategies': {
            'score_strategies': result_strategies,
            'small_unit': "8",
            'large_unit': "40"
        },
        'goals': {
            'score_goals': result_goals,
            'small_unit': "5",
            'large_unit': "25"
        },
    }


def index_clarity(answer_list):
    score = 0
    keys = [1, 4, 5, 7, 9]
    answer_list = answer_list.filter(question__row__in=keys)
    for answer in answer_list:
        score += answer.question_option.coefficient
    return score


def index_aware(answer_list):
    score = 0
    keys = [2, 6, 8, 10, 17, 34]
    answer_list = answer_list.filter(question__row__in=keys)
    for answer in answer_list:
        score += answer.question_option.coefficient
    return score


def index_impulse(answer_list):
    score = 0
    keys = [3, 14, 19, 24, 27, 32]
    answer_list = answer_list.filter(question__row__in=keys)
    for answer in answer_list:
        score += answer.question_option.coefficient
    return score


def index_nonaccept(answer_list):
    score = 0
    keys = [11, 12, 21, 23, 25, 29]
    answer_list = answer_list.filter(question__row__in=keys)
    for answer in answer_list:
        score += answer.question_option.coefficient
    return score


def index_strategies(answer_list):
    score = 0
    keys = [15, 16, 22, 28, 30, 31, 35, 36]
    answer_list = answer_list.filter(question__row__in=keys)
    for answer in answer_list:
        score += answer.question_option.coefficient
    return score


def index_goals(answer_list):
    score = 0
    keys = [13, 18, 20, 26, 33]
    answer_list = answer_list.filter(question__row__in=keys)
    for answer in answer_list:
        score += answer.question_option.coefficient
    return score


# ================================================================================

def interpretation_qli(score: float, id: int, questionnaire):
    from foundation_course.models import QuestionnaireAnswerDetail

    db_score = {}

    answer_list_part_one = QuestionnaireAnswerDetail.objects.filter(questionnaire_answer_id=id)
    id = questionnaire.dependency.id
    answer_list_part_two = QuestionnaireAnswerDetail.objects.filter(questionnaire_answer__questionnaire_id=id)

    total_balanced_score = 0
    for answer in answer_list_part_one:
        row = answer.question.row
        answer_score_part_one = answer.question_option.coefficient
        answer_score_part_two = answer_list_part_two.get(question__row=row).question_option.coefficient

        balanced_score = (answer_score_part_one - 3.5) * answer_score_part_two

        total_balanced_score += balanced_score

        db_score[row] = balanced_score

    score_quality_of_life_index = (total_balanced_score / 33) + 15

    score_health = index_health(db_score)
    score_psychological_spiritual = index_psychological_spiritual(db_score)
    score_social_economic = index_social_economic(db_score)
    score_family = index_family(db_score)

    return {
        'score_quality_of_life_index': score_quality_of_life_index,
        'score_health': score_health,
        'score_psychological_spiritual': score_psychological_spiritual,
        'score_social_economic': score_social_economic,
        'score_family': score_family,
    }


def index_health(scores: dict) -> float:
    score_health = 0
    keys = [1, 2, 3, 4, 5, 6, 7, 11, 16, 17, 18, 25, 26]
    scores_filter = {key: scores[key] for key in scores.keys() if int(key) in keys}
    for key, value in scores_filter.items():
        score_health += value

    return score_health


def index_psychological_spiritual(scores: dict) -> float:
    score_psychological_spiritual = 0
    keys = [27, 28, 29, 30, 31, 32, 33]
    scores_filter = {key: scores[key] for key in scores.keys() if int(key) in keys}
    for key, value in scores_filter.items():
        score_psychological_spiritual += value

    return score_psychological_spiritual


def index_social_economic(scores: dict) -> float:
    score_social_economic = 0
    keys = [13, 15, 19, 20, 21, 22, 23, 24]
    scores_filter = {key: scores[key] for key in scores.keys() if int(key) in keys}
    for key, value in scores_filter.items():
        score_social_economic += value

    return score_social_economic


def index_family(scores: dict) -> float:
    score_family = 0
    keys = [8, 9, 10, 12, 14]
    scores_filter = {key: scores[key] for key in scores.keys() if int(key) in keys}
    for key, value in scores_filter.items():
        score_family += value

    return score_family
