from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction

from customers.decorators import pass_foundation_course, check_practice_answer
from customers.forms import CustomerForm, PermissionStartTreatmentCustomerForm
from customers.models import Customer, CustomerDiseaseInformation
from customers.tasks.customer_activity_history import get_activity_list, get_content_customer, create_activity_history, \
    check_exercises_every_day
from customers.tasks.customers import increase_day_of_healing_period, set_time_healing_period, get_practice_answer_list, \
    check_last_day_healing_period, get_progress_charts
from customers.utility import normalize_data_filter_customer
from doctors.models import Doctor
from foundation_course.models import Questionnaire, QuestionnaireAnswer
from healing_content.forms import PracticeAnswerForm
from healing_content.models import HealingDay, PracticeAnswerDetail, PracticeAnswer
from illness.models import Illness


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class CustomerInformationDetail(View):
    def get(self, request, customer_id):
        customer = Customer.objects.get(id=customer_id)

        questionnaire_answer_list = QuestionnaireAnswer.objects.filter(customer=customer).exclude(
            questionnaire__type=4,
            questionnaire__dependencies__isnull=False
        )

        customer_activity_history_list = get_activity_list(customer)

        answers_list = get_practice_answer_list(customer)

        progress_charts = get_progress_charts(customer)

        context = {
            "customer": customer,
            "questionnaire_answer_list": questionnaire_answer_list,
            "customer_activity_history_list": customer_activity_history_list,
            "answers_list": answers_list,

            "count_charts": len(progress_charts),
            "progress_charts": progress_charts,
        }
        return render(request, 'customers/customer_detail.html', context)


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class CompletionInformationCostumer(View):
    template_name = 'customers/completion_information_customer.html'

    def get(self, request):
        doctors = Doctor.objects.all()
        customer_form = CustomerForm()
        context = {
            "doctors": doctors,
            "customer_form": customer_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            customer_new = customer_form.save(commit=False)
            customer_new.user = request.user
            customer_new.save()
            messages.success(request, "اطلاعات به درستی ثبت شد")
            return redirect('/')
        else:
            print(">>>>>>>>>>> ERRORS <<<<<<<<<<<<<<<<<< ")
            print(customer_form.errors)


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class FilterCustomer(View):
    def get(self, request):
        type_filter = request.GET['type_filter']
        if type_filter == "can_started":
            queryset = Customer.objects.filter(permission_start_treatment=True, treating_doctor=request.user.doctor)
            serializer = normalize_data_filter_customer(queryset)
            response = {
                'is_taken': True,
                'type_filter': type_filter,
                'customers': serializer,
            }
            return JsonResponse(response)
        else:
            queryset = Customer.objects.filter(permission_start_treatment=False, treating_doctor=request.user.doctor)
            serializer = normalize_data_filter_customer(queryset)
            response = {
                'is_taken': True,
                'type_filter': type_filter,
                'customers': serializer,
            }
            return JsonResponse(response)


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class DeterminingCustomerIllness(View):
    template_name = 'customers/determining_customer_illness.html'

    def get(self, request, customer_id, *args, **kwargs):
        doctor = request.user.doctor
        customer = Customer.objects.get(id=customer_id)
        treating_doctor = customer.treating_doctor
        if doctor == treating_doctor:
            illnesses = Illness.objects.all().order_by('id')
            try:
                illness_in_customer = CustomerDiseaseInformation.objects.filter(customer=customer,
                                                                                is_finished=False).first()

                context = {
                    "customer": customer,
                    "illnesses": illnesses,
                    "illness_in_customer": illness_in_customer,
                }
                return render(request, self.template_name, context)
            except:
                context = {
                    "customer": customer,
                    "illnesses": illnesses,
                }
                return render(request, self.template_name, context)
        else:
            messages.error(request, "شما مجاز به مشاهده اطلاعات این بیمار نیستید")
            return redirect('doctors:list_customers_requested')


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class OperationChoiceIllnessCustomer(View):
    def get(self, request, customer_id, illness_id, *args, **kwargs):
        doctor = request.user.doctor
        illness = Illness.objects.get(id=illness_id)
        customer = Customer.objects.get(id=customer_id)
        treating_doctor = customer.treating_doctor

        if doctor == treating_doctor:

            customer_diseasen_information = CustomerDiseaseInformation.objects.filter(
                customer=customer, is_finished=False
            )

            if not customer_diseasen_information.exists():
                CustomerDiseaseInformation.objects.create(
                    customer=customer,
                    illness=illness,
                    healing_period=illness.healingperiod
                )
                messages.success(request, "نوع بیماری مراجع مشخص شد")
                return redirect(request.META.get("HTTP_REFERER"))
            else:
                # customer_diseasen_information = customer_diseasen_information.first()
                # customer_diseasen_information.illness = illness
                # customer_diseasen_information.healing_period = illness.healingperiod
                # customer_diseasen_information.save()

                messages.error(request, "نوع بیماری را نمی توانید تغییر دهید")
                return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "شما مجاز به انتساب بیماری به این بیمار نیستید")
            return redirect('doctors:list_customers_requested')


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class PermissionStartTreatmentCustomer(View):
    def post(self, request, *args, **kwargs):
        form = PermissionStartTreatmentCustomerForm(request.POST)
        if form.is_valid():
            id, permission_start_treatment = form.cleaned_data['id'], form.cleaned_data['permission_start_treatment']
            customer = Customer.objects.get(id=id)
            customer.permission_start_treatment = True if permission_start_treatment == 'yes' else False
            customer.save()
            messages.success(request, 'تغییرات اعمال شد')
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            print(form.errors)
            return redirect(request.META.get("HTTP_REFERER"))


# ===============================================================================================
@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
@method_decorator(pass_foundation_course, name='dispatch')
class HealingPeriod(View):
    def get(self, request):
        customer = request.user.customer

        disease_information = CustomerDiseaseInformation.objects.filter(
            customer=customer,
            is_finished=False
        ).first()

        answers_list = get_practice_answer_list(customer)

        context = {
            "disease_information": disease_information,
            "answers_list": answers_list,
        }
        return render(request, 'healing_content/healing_period_page_home.html', context)

    def post(self, request):
        pass


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
@method_decorator(pass_foundation_course, name='dispatch')
# @method_decorator(has_started_healing_period, name='dispatch')
@method_decorator(check_practice_answer, name='dispatch')
class HealingPeriodCustomer(View):
    def get(self, request):
        customer = request.user.customer

        disease_information = CustomerDiseaseInformation.objects.filter(
            customer=customer,
            is_finished=False
        ).first()

        # TODO: Set time start healing period
        set_time_healing_period(disease_information)

        day = disease_information.day_of_healing_period
        healing_period = disease_information.healing_period

        # TODO: Checking whether she passed the previous day's training or not
        status, day, healing_period = check_exercises_every_day(day - 1, healing_period, customer)

        if status:
            day, healing_period = day, healing_period

        healing_day = HealingDay.objects.get(day=day, healing_period=healing_period)
        content_customer = get_content_customer(
            day=day,
            duration_of_treatment=disease_information.healing_period.duration_of_treatment,
            healing_day=healing_day
        )

        context = {
            "healing_day_id": healing_day.id,
            "healing_period_title": disease_information.healing_period.title,
            "day_of_healing_period": day,
            "disease_information": disease_information,
            "healing_content": content_customer['healing_content'],
            "questionnaires_weekly": content_customer['questionnaires_weekly'],
        }

        return render(request, 'customers/healing_period_customer.html', context)

    def post(self, request, *args, **kwargs):
        customer = request.user.customer
        form = PracticeAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            content = cd['content']
            file = cd['file']
            healing_day_id = cd['healing_day']
            with transaction.atomic():
                practice_answer = PracticeAnswer.objects.create(
                    customer=customer,
                    healing_day=healing_day_id
                )
                PracticeAnswerDetail.objects.create(
                    practice_answer=practice_answer,
                    content=content,
                    file=file
                )

                # TODO: Increase the day number of the user's healing period
                increase_day_of_healing_period(customer)

                # TODO: Checking whether it is the last day of the Healing period or not
                check_last_day_healing_period(healing_day_id, customer)

                # TODO: Register activity history for customer
                healing_day: HealingDay = HealingDay.objects.get(id=healing_day_id)
                create_activity_history(
                    customer_id=customer.id,
                    subject=f"{healing_day.healing_period}",
                    content=f"انجام تمرین های روز {healing_day.day}ام ، {healing_day.healing_period}"
                )

                messages.success(request, "جواب تمرین با موفقیت ثبت شد")
                return redirect("customers:healing_period_customer")
        else:
            messages.error(request, f"{form.errors['__all__'].as_text()}")
            return redirect("customers:healing_period_customer")


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class FoundationCourseCustomer(View):
    def get(self, request):
        questionnaire_list = Questionnaire.objects.all()

        context = {
            "questionnaire_list": questionnaire_list,
        }
        return render(request, 'customers/foundation_course_customer.html', context)


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class FollowUpCustomer(View):
    def get(self, request):
        return render(request, 'customers/follow_up_customer.html')

# ===============================================================================================
