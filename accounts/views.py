from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from doctors.models import Doctor
from .forms import LoginUserForm, RegisterCustomerForm, RegisterDoctorForm
from .decorators import login_not_required, is_staff_or_superuser
from .models import User, RoleChoices
from .utilites import phone_number_encryption
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@login_not_required
def login_page(request):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        login_form = LoginUserForm(request.POST)
        if login_form.is_valid():
            phone, password, remember_me = login_form.cleaned_data['phone'], login_form.cleaned_data['password'], \
                                           login_form.cleaned_data.get('remember_me', False)

            doctor = authenticate(request, phone=phone, password=password)
            customer = authenticate(request, phone=phone_number_encryption(phone), password=password)
            user = doctor if doctor is not None else customer
            if user:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                messages.success(request, "با موافقیت وارد شدید")

                # TODO :
                return redirect('/')



            else:
                return redirect(url)
        else:
            print(login_form.errors)
    else:
        login_form = LoginUserForm()
    context = {
        'login_form': login_form,
    }
    return render(request, "accounts/login.html", context)


@login_not_required
def register_page_customer(request):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        register_form = RegisterCustomerForm(request.POST)
        if register_form.is_valid():
            is_accept_rules = register_form.cleaned_data['is_accept_rules']
            phone = register_form.cleaned_data['phone']

            phone = phone_number_encryption(phone)

            password = register_form.cleaned_data["password"]

            if is_accept_rules:
                new_user = User.objects.create_user(phone=phone, role=RoleChoices.CUSTOMER, password=password)
                new_user.is_accept_rules = True
                new_user.save()
                messages.success(request, "کاربر با موافقیت ساخته شد")
                return redirect('accounts:login')
        else:
            print(register_form.errors)
    else:
        register_form = RegisterCustomerForm()
    context = {
        "register_form": register_form,
    }
    return render(request, "accounts/register_customer.html", context)


@login_not_required
def register_page_doctor(request):
    if request.method == "POST":
        register_form = RegisterDoctorForm(request.POST)
        if register_form.is_valid():
            is_accept_rules = register_form.cleaned_data['is_accept_rules']
            phone = register_form.cleaned_data['phone']
            password = register_form.cleaned_data["password"]
            if is_accept_rules:
                new_user = User.objects.create_user(phone=phone, role=RoleChoices.DOCTER, password=password)
                new_user.is_accept_rules = True
                new_user.save()
                messages.success(request, "کاربر با موافقیت ساخته شد")
                return redirect('accounts:login')
    else:
        register_form = RegisterCustomerForm()
    context = {
        "register_form": register_form,
    }
    return render(request, "accounts/register_doctor.html", context)


def log_out(request):
    logout(request)
    messages.success(request, "با موافقیت خارج شدید")
    return redirect('accounts:login')


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class ConfirmationDoctorByStaff(View):
    """
        Confirmation of the doctor by the site administrator or staff
    """

    @method_decorator(is_staff_or_superuser)
    def get(self, request):
        doctors = Doctor.objects.all()
        paginator = Paginator(doctors, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
            "doctors": doctors,
        }
        return render(request, 'accounts/confirmation_doctor.html', context)


