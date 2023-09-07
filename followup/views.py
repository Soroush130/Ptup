from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.db import transaction

from customers.models import CustomerDiseaseInformation
from followup.decorators import after_nine_pm
from followup.forms import FollowUpQuestionForm
from followup.models import FollowUpQuestion, FollowUpQuestionAnswer, FollowUpContent
from followup.utility import increase_follow_up_day, set_start_time_follow_up, check_question_score


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
@method_decorator(after_nine_pm, name='dispatch')
class FollowUpCustomer(View):
    template_name = 'followup/follow_up_customer.html'

    def get(self, request):
        questions = FollowUpQuestion.objects.all()

        customer = request.user.customer
        disease_information = CustomerDiseaseInformation.objects.filter(
            customer=customer,
            is_finished=False
        ).first()

        context = {
            "questions": questions,
            "day": disease_information.day_of_follow_up,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            customer = request.user.customer
            disease_information = CustomerDiseaseInformation.objects.filter(
                customer=customer,
                is_finished=False
            ).first()

            # TODO
            set_start_time_follow_up(disease_information=disease_information)

            form = FollowUpQuestionForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    question_id = form.cleaned_data.get('question_id')
                    score = form.cleaned_data.get('score')
                    day = disease_information.day_of_follow_up
                    try:
                        answer = FollowUpQuestionAnswer.objects.get(question_id=question_id, customer=customer,
                                                                    day=day)
                        answer.score = score
                        answer.save()
                        messages.success(request, f"نمره سوال {answer.question.row} بروزرسانی شد")

                        # TODO: check score
                        status = check_question_score(question_id, answer.question.structure_evaluated, day, customer)
                        if status:
                            return redirect('follow_up:show_content')

                    except FollowUpQuestionAnswer.DoesNotExist:
                        answer_new = FollowUpQuestionAnswer.objects.create(
                            question_id=question_id,
                            customer=customer,
                            score=score,
                            day=day
                        )

                        # TODO
                        increase_follow_up_day(request=request, disease_information=disease_information)

                        messages.success(request, f"نمره سوال {answer_new.question.row} ثبت شد")

                        # TODO: check score
                        status = check_question_score(question_id, answer_new.question.structure_evaluated, day,
                                                      customer)
                        if status:
                            return redirect('follow_up:show_content')


            else:
                messages.error(request, f"{form.errors.__all__}")

            return redirect('follow_up:follow_up_customer')


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class ShowContentFollowUp(View):
    def get(self, request):
        structure_evaluated = request.GET.get("structure_evaluated", 'S')
        videos = FollowUpContent.objects.filter(structure_evaluated=structure_evaluated)
        context = {
            "videos": videos
        }
        return render(request, 'followup/follow_up_contents.html', context)
