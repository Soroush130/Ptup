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
        # TODO : check
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


# ================================  MEDI  ======================================
def interpretation_medi(score: float, id: int):
    from foundation_course.models import QuestionnaireAnswerDetail
    answer_list = QuestionnaireAnswerDetail.objects.filter(questionnaire_answer_id=id)

    result_irritable_mood = index_irritable_mood(answer_list=answer_list)
    result_positive_mood = index_positive_mood(answer_list=answer_list)
    result_depressed_mood = index_depressed_mood(answer_list=answer_list)
    result_spontaneous_arousal = index_spontaneous_arousal(answer_list=answer_list)
    result_physical_anxiety = index_physical_anxiety(answer_list=answer_list)
    result_social_anxiety = index_social_anxiety(answer_list=answer_list)
    result_disturbing_thoughts = index_disturbing_thoughts(answer_list=answer_list)
    result_re_traumatic_experience = index_re_traumatic_experience(answer_list=answer_list)
    result_avoid = index_avoid(answer_list=answer_list)

    return {
        "irritable_mood": result_irritable_mood,
        "positive_mood": result_positive_mood,
        "depressed_mood": result_depressed_mood,
        "spontaneous_arousal": result_spontaneous_arousal,
        "physical_anxiety": result_physical_anxiety,
        "social_anxiety": result_social_anxiety,
        "disturbing_thoughts": result_disturbing_thoughts,
        "re_traumatic_experience": result_re_traumatic_experience,
        "avoid": result_avoid,
    }


def calc_score_selected_questions_in_questionnaire_medi(keys, answer_list):
    """
    Calculate the score of selected questions in a questionnaire
    :param keys:
    :param answer_list:
    :return: score
    """
    score = 0
    answer_list = answer_list.filter(question__row__in=keys)
    for answer in answer_list:
        score += answer.question_option.coefficient
    return score


def index_irritable_mood(answer_list):
    """
    خلق و خوی روان‌ آزرده
    """
    keys = [1, 10, 16, 32, 35]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)


def index_positive_mood(answer_list):
    """
        خلق و خوی مثبت
    """
    keys = [2, 17, 24, 33, 36]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)


def index_depressed_mood(answer_list):
    """
        خلق افسرده
    """
    keys = [3, 11, 25, 37, 43]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)


def index_spontaneous_arousal(answer_list):
    """
        برانگیختگی خودانگیخته
    """
    keys = [4, 13, 18, 26, 44]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)


def index_physical_anxiety(answer_list):
    """
        اضطراب جسمانی
    """
    keys = [6, 19, 28, 38, 45]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)


def index_social_anxiety(answer_list):
    """
        اضطراب اجتماعی
    """
    keys = [7, 14, 22, 41, 47]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)


def index_disturbing_thoughts(answer_list):
    """
        افکار مزاحم
    """
    keys = [5, 12, 21, 30, 40, 46]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)


def index_re_traumatic_experience(answer_list):
    """
        تجربۀ مجدد تروماتیک
    """
    keys = [8, 20, 29, 39, 48]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)


def index_avoid(answer_list):
    """
    اجتناب
    """
    keys = [9, 15, 23, 27, 31, 34, 42, 49]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)


# ================================  NEO  ======================================
def interpretation_neo(id: int):
    from foundation_course.models import QuestionnaireAnswerDetail
    answer_list = QuestionnaireAnswerDetail.objects.filter(questionnaire_answer_id=id)

    result_nervousness = index_nervousness(answer_list=answer_list)
    result_being_extroverted = index_being_extroverted(answer_list=answer_list)
    result_openness = index_openness(answer_list=answer_list)
    result_agree = index_agree(answer_list=answer_list)
    result_conscientiousness = index_conscientiousness(answer_list=answer_list)

    return {
        "nervousness": result_nervousness,
        "being_extroverted": result_being_extroverted,
        "openness": result_openness,
        "agree": result_agree,
        "conscientiousness": result_conscientiousness,
    }


def calc_score_selected_questions_in_questionnaire_neo(keys, answer_list):
    """
    Calculate the score of selected questions in a questionnaire
    :param keys:
    :param answer_list:
    :return: score
    """
    score = 0
    answer_list = answer_list.filter(question__row__in=keys)
    for answer in answer_list:
        score += answer.question_option.coefficient
    return score


def index_nervousness(answer_list):
    keys = [1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)


def index_being_extroverted(answer_list):
    keys = [2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)


def index_openness(answer_list):
    keys = [3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)


def index_agree(answer_list):
    keys = [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)


def index_conscientiousness(answer_list):
    keys = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    return calc_score_selected_questions_in_questionnaire_medi(keys=keys, answer_list=answer_list)
