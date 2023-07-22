from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages

from customers.forms import CustomerForm
from doctors.models import Doctor


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