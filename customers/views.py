from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from customers.forms import CustomerForm, CustomerIllnessForm, PermissionStartTreatmentCustomerForm
from customers.models import Customer
from customers.utility import normalize_data_filter_customer
from doctors.models import Doctor
from illness.models import Illness


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
            illnesses = Illness.objects.all()
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
            # TODO: بعد از نوشتن مدل اطلاعات بیماری هر مشتری این قسمت تکمیل شود
            print(customer, '\n', illness)
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
