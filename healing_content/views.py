from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction

from healing_content.forms import DayFeedbackForm
from healing_content.models import PracticeAnswer, PracticeAnswerDetail, DayFeedback


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class DayFeedbackView(View):
    def get(self, request, practice_answer_id, *args, **kwargs):
        practice_answer = PracticeAnswer.objects.get(id=practice_answer_id)
        practice_answer_details = PracticeAnswerDetail.objects.get(practice_answer=practice_answer)
        answer = {
            'content': practice_answer_details.content if practice_answer_details.content is not None else "پیامی ثبت نکرده است",
            'status_file': True if practice_answer_details.file else False,
            'file': practice_answer_details.file.url if practice_answer_details.file else ''
        }

        context = {
            "practice_answer_id": practice_answer.id,
            "time_answer": practice_answer.time_answer,
            "answer": answer,
        }
        return render(request, 'healing_content/day_feedback_detail.html', context)


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class CreateFeedbackView(View):
    def post(self, request, *args, **kwargs):
        form = DayFeedbackForm(request.POST)
        if form.is_valid():
            practice_answer_id = form.cleaned_data.get('practice_answer_id')
            subject = form.cleaned_data.get('subject')
            content = form.cleaned_data.get('content')

            DayFeedback.objects.create(
                practice_answer_id=practice_answer_id,
                doctor=request.user.doctor,
                subject=subject,
                content=content
            )
            messages.success(request, 'بازخورد ثبت شد')
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, f"{form.errors.as_text()}")
            return redirect(request.META.get("HTTP_REFERER"))
