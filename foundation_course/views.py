from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db import transaction

from customers.tasks.customer_activity_history import create_activity_history
from foundation_course.decorators import questionnaire_completion
from foundation_course.models import Questionnaire, Question, QuestionnaireAnswer, QuestionnaireAnswerDetail
from foundation_course.tasks.foundation_course import check_foundation_course
from foundation_course.tasks.questionnaire import get_list_answer_questionnaire, check_suicide
from foundation_course.utility import calculate_score_each_questionnaire


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
@method_decorator(questionnaire_completion, name='dispatch')
class QuestionnaireDetail(View):
    def get(self, request, id):
        questionnaire = Questionnaire.objects.get(id=id)

        number_of_option = "".join([str(i) for i in range(1, questionnaire.number_of_options + 1)])

        questions = Question.objects.filter(questionnaire=questionnaire).order_by('row')

        context = {
            "questionnaire": questionnaire,
            "number_of_option": number_of_option,
            "questions": questions,
            "questions_count": questions.count(),
        }
        return render(request, 'foundation_course/questionnaire_detail.html', context)


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class CompleteQuestionnaireByCustomer(View):
    def post(self, request):
        if request.method == "POST":
            customer = request.user.customer
            questionnaire_id = request.POST['questionnaire_id']
            questions_count = request.POST['questions_count']
            questionnaire = Questionnaire.objects.get(id=questionnaire_id)
            with transaction.atomic():

                selected_answers = get_list_answer_questionnaire(request.POST.items())

                if int(questions_count) == len(selected_answers.keys()):

                    questionnaire_answer = QuestionnaireAnswer.objects.create(
                        questionnaire=questionnaire,
                        customer=customer
                    )

                    objects_to_create = []
                    for key, value in selected_answers.items():
                        objects_to_create.append(QuestionnaireAnswerDetail(
                            questionnaire_answer=questionnaire_answer,
                            question_id=key,
                            question_option_id=value
                        ))

                    answers_list = QuestionnaireAnswerDetail.objects.bulk_create(objects_to_create)

                    calculate_score_each_questionnaire(questionnaire_answer, answers_list)

                    # TODO: Register activity history
                    create_activity_history(customer.id, 'تکمیل پرسشنامه',
                                            f'تکمیل پرسشنامه : {questionnaire_answer.questionnaire.__str__()}')

                    # TODO: Let's check if the client is trying to commit suicide or not
                    if questionnaire.type == 2:
                        check_suicide(9, questionnaire_answer.id, customer)

                    messages.success(request, "پرسشنامه به درستی تکمیل شد")

                    # TODO: Checking the end of the foundation course
                    status_foundation_course = check_foundation_course(request, customer.id)
                    if status_foundation_course:
                        return redirect('home')

                    return redirect('customers:foundation_course_customer')
                else:
                    messages.error(request, "لطفا پرسشنامه را تکمیل کنید")
                    return redirect(request.META.get("HTTP_REFERER"))
