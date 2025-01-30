from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages

from question_answer_app.forms import QuestionForm, AnswerForm
from question_answer_app.models import Question, Answer


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class QuestionView(View):
    def get(self, request, *args, **kwargs):
        if request.user.customer.permission_ask_question:
            questions = Question.objects.filter(customer=request.user.customer).order_by('-created_at')
            context = {
                "questions": questions,
            }
            return render(request, 'question_answer_app/question.html', context)
        else:
            messages.error(request, "شما دسترسی سوال پرسیدن ندارید")
            return redirect('home')


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class QuestionDetailView(View):
    def get(self, request, question_id, *args, **kwargs):
        question = Question.objects.filter(id=question_id).first()
        question_answers = Answer.objects.filter(question_id=question_id).order_by('-created_at')
        context = {
            'question': question,
            'question_answers': question_answers,
            'flag': True if request.user.role == 1 else False,
        }
        return render(request, 'question_answer_app/question_detail.html', context)


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class AnswerView(View):
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor
        questions = Question.objects.filter(doctor=doctor).order_by('-created_at')

        context = {
            "questions": questions,
        }
        return render(request, 'question_answer_app/answer.html', context)


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class SubmitAnswerView(View):
    def post(self, request, question_id, *args, **kwargs):
        answer_form = AnswerForm(request.POST, request.FILES)
        if answer_form.is_valid():
            answer = answer_form.cleaned_data['answer_text']
            Answer.objects.create(
                question_id=question_id,
                answer_text=answer
            )
            messages.success(request, "جواب شما ثبت شد")
            return redirect('question_answer:answer')
        else:
            messages.error(request, "فرم را به درستی پر کنید")
            return redirect('question_answer:answer')


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class SubmitQuestionView(View):
    def post(self, request, *args, **kwargs):
        question_form = QuestionForm(request.POST, request.FILES)

        if question_form.is_valid():
            question = question_form.cleaned_data['question_text']
            Question.objects.create(
                customer=request.user.customer,
                doctor=request.user.customer.treating_doctor,
                question_text=question
            )
            messages.success(request, "سوال شما ثبت شد")
            return redirect('question_answer:question')
        else:
            messages.error(request, "فرم را به درستی پر کنید")
            return redirect('question_answer:question')
