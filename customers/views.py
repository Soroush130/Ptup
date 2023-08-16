from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse

from customers.decorators import pass_foundation_course
from customers.forms import CustomerForm, PermissionStartTreatmentCustomerForm
from customers.models import Customer, CustomerDiseaseInformation, CustomerActivityHistory
from customers.tasks.customer_activity_history import get_activity_list
from customers.utility import normalize_data_filter_customer
from doctors.models import Doctor
from foundation_course.models import Questionnaire, QuestionnaireAnswer
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

        context = {
            "customer": customer,
            "questionnaire_answer_list": questionnaire_answer_list,
            "customer_activity_history_list": customer_activity_history_list,
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
class HealingPeriodCustomer(View):
    def get(self, request):
        customer = request.user.customer

        disease_information = CustomerDiseaseInformation.objects.filter(
            customer=customer,
            is_finished=False
        ).first()

        context = {
            "disease_information": disease_information,
        }

        return render(request, 'customers/healing_period_customer.html', context)


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
