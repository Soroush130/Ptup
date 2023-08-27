from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction

from customers.tasks.customer_activity_history import create_activity_history
from customers.tasks.customers import increase_day_of_healing_period, check_last_day_healing_period
from foundation_course.tasks.questionnaire import get_list_answer_questionnaire
from foundation_course.utility import calculate_score_each_questionnaire_weekly
from healing_content.forms import DayFeedbackForm
from healing_content.models import DayFeedback, QuestionnaireWeek, QuestionWeek, \
    QuestionnaireWeekAnswer, QuestionnaireWeekAnswerDetail


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class DayFeedbackView(View):
    def get(self, request, practice_answer_id, *args, **kwargs):
        # TODO : Check
        # practice_answer = PracticeAnswer.objects.get(id=practice_answer_id)
        practice_answer = None
        # practice_answer_details = PracticeAnswerDetail.objects.get(practice_answer=practice_answer)
        practice_answer_details = None
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


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class ShowFeedbackByCustomerView(View):
    def get(self, request, practice_answer_id, *args, **kwargs):
        customer = request.user.customer
        doctor = customer.treating_doctor
        try:
            day_feedback = DayFeedback.objects.get(
                practice_answer_id=practice_answer_id,
                doctor=doctor,
                practice_answer__customer=customer
            )

            context = {
                "status": True,
                "day_feedback": day_feedback,
            }
            return render(request, 'healing_content/show_feed_back_by_customer.html', context)
        except DayFeedback.DoesNotExist:
            context = {
                "status": False,
                "doctor": doctor,
                "day_feedback": "هیچ بازخوردی ثبت نشده است",
            }
            return render(request, 'healing_content/show_feed_back_by_customer.html', context)


# =============================== Questionnaire Weekly ========================
@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class QuestionnaireWeeklyView(View):
    def get(self, request, questionnaire_id, healing_day_id, *args, **kwargs):
        questionnaire_week = QuestionnaireWeek.objects.get(id=questionnaire_id)

        number_of_option = "".join([str(i) for i in range(1, questionnaire_week.number_of_options + 1)])

        questions = QuestionWeek.objects.filter(questionnaire_week=questionnaire_week).order_by('row')

        context = {
            "healing_day_id": healing_day_id,
            "questionnaire": questionnaire_week,
            "number_of_option": number_of_option,
            "questions": questions,
            "questions_count": questions.count(),
        }
        return render(request, 'healing_content/questionnaire_weekly_detail.html', context)


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class CompleteQuestionnaireWeeklyByCustomer(View):
    def post(self, request):
        if request.method == "POST":
            customer = request.user.customer
            healing_day_id = request.POST['healing_day_id']
            questionnaire_id = request.POST['questionnaire_id']
            questions_count = request.POST['questions_count']
            questionnaire = QuestionnaireWeek.objects.get(id=questionnaire_id)
            with transaction.atomic():

                selected_answers = get_list_answer_questionnaire(request.POST.items())

                if int(questions_count) == len(selected_answers.keys()):

                    questionnaire_answer = QuestionnaireWeekAnswer.objects.create(
                        questionnaire_week=questionnaire,
                        customer=customer,
                        healing_day_id=healing_day_id
                    )

                    objects_to_create = []
                    for key, value in selected_answers.items():
                        objects_to_create.append(QuestionnaireWeekAnswerDetail(
                            questionnaire_week=questionnaire_answer,
                            question_week_id=key,
                            question_option_week_id=value
                        ))

                    answers_list = QuestionnaireWeekAnswerDetail.objects.bulk_create(objects_to_create)

                    calculate_score_each_questionnaire_weekly(questionnaire_answer, answers_list)

                    # TODO: Increase the day number of the user's healing period
                    increase_day_of_healing_period(customer)

                    # TODO: Checking whether it is the last day of the Healing period or not
                    check_last_day_healing_period(request, healing_day_id, customer)

                    # TODO: Register activity history
                    create_activity_history(customer.id, 'تکمیل پرسشنامه هفتگی',
                                            f'تکمیل پرسشنامه هفتگی : {questionnaire_answer.questionnaire_week.__str__()}')

                    return redirect(f'/content/questionnaire_weekly/{questionnaire_id}/{healing_day_id}/')
                else:
                    messages.error(request, "لطفا پرسشنامه را تکمیل کنید")
                    return redirect(request.META.get("HTTP_REFERER"))
