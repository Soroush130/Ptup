from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from customers.forms import CustomerForm
from customers.models import Customer
from customers.utility import normalize_data_filter_customer
from doctors.models import Doctor


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
            queryset = Customer.objects.filter(permission_start_treatment=True)
            serializer = normalize_data_filter_customer(queryset)
            response = {
                'is_taken': True,
                'type_filter': type_filter,
                'customers': serializer,
            }
            return JsonResponse(response)
        else:
            queryset = Customer.objects.filter(permission_start_treatment=False)
            serializer = normalize_data_filter_customer(queryset)
            response = {
                'is_taken': True,
                'type_filter': type_filter,
                'customers': serializer,
            }
            return JsonResponse(response)
