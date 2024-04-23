from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction

from customers.decorators import pass_foundation_course, not_pass_healing_period, has_permission_start_treatment
from customers.forms import CustomerForm, PermissionStartTreatmentCustomerForm
from customers.models import Customer, CustomerDiseaseInformation
from customers.tasks.customer_activity_history import get_activity_list, create_activity_history, \
    get_practices_healing_week, get_questionnaire_weekly
from customers.tasks.customers import increase_week_of_healing_period, get_practice_answer_list, \
    check_last_day_healing_period, get_progress_charts, group_by_healing_content_each_week, set_time_healing_period
from customers.utility import normalize_data_filter_customer
from doctors.models import Doctor
from foundation_course.models import Questionnaire, QuestionnaireAnswer
from foundation_course.tasks.questionnaire import get_list_answer_questionnaire
from healing_content.models import HealingWeek, AnswerPractice
from illness.models import Illness
from ptup_utilities.utility import show_custom_errors


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
            "customer_id": customer_id,
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
        doctors = Doctor.objects.filter(is_verify=True)
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
            error_message = show_custom_errors(customer_form.errors)
            messages.error(request, error_message)
            return redirect(request.META.get("HTTP_REFERER"))


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
        _URL = request.META.get("HTTP_REFERER")

        doctor = request.user.doctor
        illness = Illness.objects.get(id=illness_id)
        customer = Customer.objects.get(id=customer_id)
        treating_doctor = customer.treating_doctor

        if doctor == treating_doctor:

            customer_diseasen_information = CustomerDiseaseInformation.objects.filter(
                customer=customer, is_finished=False
            )

            if not customer_diseasen_information.exists():
                try:
                    CustomerDiseaseInformation.objects.create(
                        customer=customer,
                        illness=illness,
                        healing_period=illness.healingperiod
                    )
                    messages.success(request, "نوع بیماری مراجع مشخص شد")
                    return redirect(_URL)
                except:
                    messages.error(request, "دوره درمانی برای این بیماری وجود ندارد")
                    return redirect(_URL)
            else:
                messages.error(request, "نوع بیماری را نمی توانید تغییر دهید")
                return redirect(_URL)
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
            # print(form.errors)
            return redirect(request.META.get("HTTP_REFERER"))


# ===============================================================================================
@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
@method_decorator(has_permission_start_treatment, name='dispatch')
class FoundationCourseCustomer(View):
    def get(self, request):
        with transaction.atomic():
            disease_information = CustomerDiseaseInformation.objects.filter(
                customer=request.user.customer,
                is_finished=False
            ).first()

            # set time start period
            if disease_information.start_time_foundation_course is None:
                disease_information.start_time_foundation_course = timezone.now()
                disease_information.save()

        questionnaire_list = Questionnaire.objects.all()

        context = {
            "questionnaire_list": questionnaire_list,
        }
        return render(request, 'customers/foundation_course_customer.html', context)


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
@method_decorator(pass_foundation_course, name='dispatch')
@method_decorator(not_pass_healing_period, name='dispatch')
class HealingContentEachWeek(View):
    def get(self, request):
        _URL = request.META.get("HTTP_REFERER")
        with transaction.atomic():
            customer = request.user.customer

            disease_information = CustomerDiseaseInformation.objects.filter(
                customer=customer,
                is_finished=False
            ).first()

            # TODO: set time start period
            set_time_healing_period(disease_information)
            # if disease_information.start_time_period is None:
            #     disease_information.start_time_period = timezone.now()
            #     disease_information.save()

            week = disease_information.week_of_healing_period
            try:
                healing_week = HealingWeek.objects.get(week=week, healing_period=disease_information.healing_period)
                contents_in_week = group_by_healing_content_each_week(healing_week)

                context = {
                    'week': week,
                    'healing_week': healing_week,
                    'disease_information': disease_information,
                    'contents': contents_in_week,
                }
                return render(request, 'healing_content/healing_period_each_week.html', context)
            except HealingWeek.DoesNotExist:
                messages.error(request, "هقته درمانی تعریف نشده است")
                return redirect(_URL)



@login_required(login_url="accounts:login")
@pass_foundation_course
@not_pass_healing_period
def practice_each_week(request, practice_each_week_id):
    customer = request.user.customer

    disease_information = CustomerDiseaseInformation.objects.filter(
        customer=customer,
        is_finished=False
    ).first()

    healing_week = HealingWeek.objects.get(id=practice_each_week_id)

    practices = get_practices_healing_week(healing_week)

    questionnaires_weekly, questionnaires_weekly_count = get_questionnaire_weekly(
        disease_information=disease_information,
        duration_of_treatment=healing_week.healing_period.duration_of_treatment
    )
    context = {
        'week': healing_week.week,
        'healing_week_id': healing_week.id,
        'practices': practices,
        'questionnaires_weekly': questionnaires_weekly,
    }
    return render(request, 'healing_content/completion_practice_each_week.html', context)


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
@method_decorator(pass_foundation_course, name='dispatch')
@method_decorator(not_pass_healing_period, name='dispatch')
class CompletionPractice(View):
    def post(self, request, *args, **kwargs):
        customer = request.user.customer
        if request.method == "POST":
            selected_answers = get_list_answer_questionnaire(request.POST.items())
            healing_week_id = request.POST['healing_week_id']

            with transaction.atomic():
                objects_to_create = []
                for question_practice_id, answer in selected_answers.items():
                    if answer != "":
                        answer_practice = AnswerPractice.objects.filter(customer=customer,
                                                                        healing_week_id=healing_week_id,
                                                                        question_practice_id=question_practice_id)
                        if not answer_practice.exists():
                            objects_to_create.append(
                                AnswerPractice(customer=customer, healing_week_id=healing_week_id,
                                               question_practice_id=question_practice_id, answer=answer)
                            )
                        else:
                            answer_practice = answer_practice.first()
                            answer_practice.answer = answer
                            answer_practice.save()
                            messages.success(request, "جواب تمرین بروزرسانی شد")
                    else:
                        messages.error(request, "لطفا تمرین ها پر کنید")
                        return redirect(request.META.get("HTTP_REFERER"))

                AnswerPractice.objects.bulk_create(objects_to_create)

                # TODO: Register activity history for customer
                healing_week: HealingWeek = HealingWeek.objects.get(id=healing_week_id)
                create_activity_history(
                    customer_id=customer.id,
                    subject=f"{healing_week.healing_period}",
                    content=f"انجام تمرین های هفته {healing_week.week}ام ، {healing_week.healing_period}"
                )

                # TODO: Increase the day number of the user's healing period
                increase_week_of_healing_period(request, customer)

                # TODO: Checking whether it is the last day of the Healing period or not
                check_last_day_healing_period(request, healing_week_id, customer)

                return redirect(request.META.get("HTTP_REFERER"))
        else:
            return redirect("customers:healing_period_customer")


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class HealingContentMap(View):
    def get(self, request, *args, **kwargs):
        try:
            customer = request.user.customer
            disease_information = CustomerDiseaseInformation.objects.filter(
                customer=customer,
                is_finished=False
            ).first()

            answers_list = get_practice_answer_list(customer)

            context = {
                "customer_id": customer.id,
                "answers_list": answers_list,
                "disease_information": disease_information,
            }
            return render(request, 'healing_content/healing_content_map.html', context)
        except:
            messages.error(request, "پرونده درمانی برای شما یافت نشد")
            return redirect('home')

# ===============================================================================================
