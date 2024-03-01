from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db import transaction

from customers.models import Customer
from customers.tasks.customer_activity_history import create_activity_history
from customers.tasks.customers import increase_week_of_healing_period, check_last_day_healing_period
from foundation_course.tasks.questionnaire import get_list_answer_questionnaire
from foundation_course.utility import calculate_score_each_questionnaire_weekly
from healing_content.forms import DayFeedbackForm
from healing_content.models import DayFeedback, QuestionnaireWeek, QuestionWeek, \
    QuestionnaireWeekAnswer, QuestionnaireWeekAnswerDetail, AnswerPractice


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class DayFeedbackView(View):
    def get(self, request, customer_id, healing_week_id, *args, **kwargs):
        user_role = request.user.role
        try:
            customer = Customer.objects.get(id=customer_id)
            answer_practice_list = AnswerPractice.objects.filter(customer=customer, healing_week_id=healing_week_id)

            context = {
                "user_role": user_role,
                "answer_practice_list": answer_practice_list,
            }
            return render(request, 'healing_content/day_feedback_detail.html', context)
        except Customer.DoesNotExist:
            pass


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class CreateFeedbackView(View):
    def post(self, request, *args, **kwargs):
        form = DayFeedbackForm(request.POST)
        if form.is_valid():
            answer_practice_id = form.cleaned_data.get('answer_practice_id')
            subject = form.cleaned_data.get('subject')
            content = form.cleaned_data.get('content')
            with transaction.atomic():
                try:
                    day_feedback = DayFeedback.objects.get(practice_answer_id=answer_practice_id)

                    day_feedback.subject = subject
                    day_feedback.content = content
                    day_feedback.save()
                    messages.success(request, 'بازخورد بروزرسانی شد')
                    return redirect(request.META.get("HTTP_REFERER"))

                except DayFeedback.DoesNotExist:
                    DayFeedback.objects.create(
                        practice_answer_id=answer_practice_id,
                        doctor=request.user.doctor,
                        subject=subject,
                        content=content
                    )
                    messages.success(request, 'بازخورد ثبت شد')
                    return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, f"{form.errors.as_text()}")
            return redirect(request.META.get("HTTP_REFERER"))


# =============================== Questionnaire Weekly ========================
@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class QuestionnaireWeeklyView(View):
    def get(self, request, questionnaire_id, healing_week_id, *args, **kwargs):
        questionnaire_week = QuestionnaireWeek.objects.get(id=questionnaire_id)

        number_of_option = "".join([str(i) for i in range(1, questionnaire_week.number_of_options + 1)])

        questions = QuestionWeek.objects.filter(questionnaire_week=questionnaire_week).order_by('row')

        context = {
            "healing_week_id": healing_week_id,
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
            healing_week_id = request.POST['healing_week_id']
            questionnaire_id = request.POST['questionnaire_id']
            questions_count = request.POST['questions_count']
            questionnaire = QuestionnaireWeek.objects.get(id=questionnaire_id)
            with transaction.atomic():

                selected_answers = get_list_answer_questionnaire(request.POST.items())

                if int(questions_count) == len(selected_answers.keys()):
                    questionnaire_answer = QuestionnaireWeekAnswer.objects.create(
                        questionnaire_week=questionnaire,
                        customer=customer,
                        healing_week_id=healing_week_id
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
                    increase_week_of_healing_period(request, customer)

                    # TODO: Checking whether it is the last day of the Healing period or not
                    check_last_day_healing_period(request, healing_week_id, customer)

                    # TODO: Register activity history
                    create_activity_history(customer.id, 'تکمیل پرسشنامه هفتگی',
                                            f'تکمیل پرسشنامه هفتگی : {questionnaire_answer.questionnaire_week.__str__()}')

                    return redirect('customers:healing_period_each_week')
                else:
                    messages.error(request, "لطفا پرسشنامه را تکمیل کنید")
                    return redirect(request.META.get("HTTP_REFERER"))
