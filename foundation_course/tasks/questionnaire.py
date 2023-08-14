def get_list_answer_questionnaire(items):
    selected_answers = {}
    for key, value in items:
        if key.startswith('answer'):
            question_id = key[len('answer'):]
            selected_answers[question_id] = value

    return selected_answers