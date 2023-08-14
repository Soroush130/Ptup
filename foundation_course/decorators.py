from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

from foundation_course.models import QuestionnaireAnswer

import re


def questionnaire_completion(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        path = request.path
        pattern = r"/(\d+)/"
        match = re.search(pattern, path)
        if match:
            number = match.group(1)
            customer = request.user.customer

            questionnaire_answer_list_each_customr = QuestionnaireAnswer.objects.filter(
                customer=customer,
                questionnaire_id=number
            )
            if not questionnaire_answer_list_each_customr.exists():
                return view_func(request, *args, **kwargs)
            else:
                messages.info(request, "شما این پرسشنامه را تکمیل کرده اید")
                return redirect('customers:foundation_course_customer')

    return wrapped_view
