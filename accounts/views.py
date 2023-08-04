from datetime import timedelta

from django.contrib.auth import login, authenticate, logout
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils import timezone

from doctors.models import Doctor
from ptup_utilities.utility import set_session, get_session
from .forms import LoginUserForm, RegisterCustomerForm, RegisterDoctorForm, OtpCodeForm
from .decorators import login_not_required, is_staff_or_superuser, is_otp_code_verify, check_last_otp_code_user
from .models import User, RoleChoices, OtpCode
from .senders import SmsSender
from .utilites import phone_number_encryption, generate_otp_code, create_otp_code, sms
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
                return redirect('/')
            else:
                messages.info(request, "کاربری پیدا نشد")
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

            phone_encryption = phone_number_encryption(phone)

            password = register_form.cleaned_data["password"]

            if is_accept_rules:
                new_user = User.objects.create_user(
                    phone=phone_encryption,
                    role=RoleChoices.CUSTOMER,
                    password=password
                )

                new_user.is_accept_rules = True
                new_user.is_active = False
                new_user.save()

                otp_code: str = generate_otp_code(5)
                OtpCode.objects.create(
                    phone=phone_encryption,
                    otp_code=otp_code
                )

                # set session
                set_session(request, "phone", phone)
                set_session(request, "role", RoleChoices.CUSTOMER)
                set_session(request, "previous_url", request.META.get('HTTP_REFERER'))

                result = sms(request=request, phone=phone, otp_code=otp_code)
                if result:
                    return redirect('accounts:confirm_otp')
                else:
                    return redirect('accounts:register_doctor')
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
                new_user = User.objects.create_user(
                    phone=phone,
                    role=RoleChoices.DOCTER,
                    password=password
                )
                new_user.is_accept_rules = True
                new_user.is_active = False
                new_user.save()

                otp_code: str = generate_otp_code(5)
                OtpCode.objects.create(
                    phone=phone,
                    otp_code=otp_code
                )

                # set session
                set_session(request, "phone", phone)
                set_session(request, "role", RoleChoices.DOCTER)
                set_session(request, "previous_url", request.META.get('HTTP_REFERER'))

                result = sms(request=request, phone=phone, otp_code=otp_code)
                if result:
                    return redirect('accounts:confirm_otp')
                else:
                    return redirect('accounts:register_doctor')
    else:
        register_form = RegisterCustomerForm()
    context = {
        "register_form": register_form,
    }
    return render(request, "accounts/register_doctor.html", context)


@method_decorator(login_not_required, name='dispatch')
@method_decorator(is_otp_code_verify, name='dispatch')
class ConfirmOtpCodeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'accounts/otp_code.html', context)

    def post(self, request, *args, **kwargs):
        otp_form = OtpCodeForm(request.POST)
        if otp_form.is_valid():
            otp_code = otp_form.cleaned_data['otp_code']
            current_time = timezone.now()
            is_otp_code = OtpCode.objects.get(
                otp_code=otp_code,
                created__lt=current_time,
                created__gt=current_time - timedelta(seconds=120),
                is_valid=False
            )
            if is_otp_code:
                with transaction.atomic():
                    is_otp_code.is_valid = True
                    is_otp_code.save()

                    user = User.objects.get(phone=is_otp_code.phone)
                    user.is_active = True
                    user.is_otp_code_verify = True
                    user.save()

                    messages.success(request, "کد اعتبارسنجی صحیح بود")
                    return redirect('accounts:login')
            else:
                messages.info(request, "کد منقضی شده است")
                return redirect(request.META.get("HTTP_REFERER"))
        else:
            msg = otp_form['otp_code'].errors
            messages.error(request, msg)
            return redirect(request.META.get("HTTP_REFERER"))


@method_decorator(login_not_required, name='dispatch')
@method_decorator(is_otp_code_verify, name='dispatch')
@method_decorator(check_last_otp_code_user, name='dispatch')
class ReSendOtpCodeView(View):
    def get(self, request):
        phone = get_session(request, 'phone')

        user = User.objects.get(phone__exact=phone)
        user_role = user.role
        DOCTOR = 1

        if user_role == DOCTOR:

            otp_code: str = generate_otp_code(5)
            create_otp_code(phone=phone, otp_code=otp_code)

            result = sms(request=request, phone=phone, otp_code=otp_code)
            if result:
                return redirect('accounts:confirm_otp')
            else:
                return redirect('accounts:register_doctor')
        else:

            phone_encryption = phone_number_encryption(phone)

            otp_code: str = generate_otp_code(5)
            create_otp_code(phone=phone_encryption, otp_code=otp_code)

            result = sms(request=request, phone=phone, otp_code=otp_code)
            if result:
                return redirect('accounts:confirm_otp')
            else:
                return redirect('accounts:register_doctor')


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
