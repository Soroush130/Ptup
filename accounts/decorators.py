from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps
from django.utils import timezone
from accounts.models import User, OtpCode
from accounts.utilites import phone_number_encryption
from ptup_utilities.utility import get_session
import datetime


def login_not_required(view_func):
    """
    This function is used to check if the user is anonymous
    :param view_func:
    :return wrapped_view:
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')

    return wrapped_view


def is_staff_or_superuser(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "شما دسترسی لازم را ندارید")
            return redirect('/')

    return wrapped_view


def is_otp_code_verify(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.session.has_key('phone'):
            phone = get_session(request, 'phone')
            role = get_session(request, 'role')
            try:
                if role == 1:
                    user = User.objects.get(phone__exact=phone)
                else:
                    user = User.objects.get(phone__exact=phone_number_encryption(phone))
                if not user.is_otp_code_verify:
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect(get_session(request, 'previous_url'))
            except:
                return redirect(get_session(request, 'previous_url'))
        else:
            return redirect(get_session(request, 'previous_url'))

    return wrapped_view


def check_last_otp_code_user(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        global permission_request_otp_code
        current_time = timezone.now()
        if request.session.has_key('phone'):
            phone = get_session(request, 'phone')
            role = get_session(request, 'role')
            try:
                if role == 1:
                    list_otp_code = OtpCode.objects.filter(phone__exact=phone)
                    result = []
                    for code in list_otp_code:
                        created = code.created
                        if created < current_time < created + datetime.timedelta(seconds=120):
                            result.append(code.otp_code)

                    print(result)

                    if result != []:
                        permission_request_otp_code = False
                    else:
                        permission_request_otp_code = True


                else:
                    list_otp_code = OtpCode.objects.filter(phone__exact=phone_number_encryption(phone))
                    result = []
                    for code in list_otp_code:
                        created = code.created
                        if created < current_time < created + datetime.timedelta(seconds=120):
                            result.append(code.otp_code)

                    print(result)

                    if result != []:
                        permission_request_otp_code = False
                    else:
                        permission_request_otp_code = True

                if permission_request_otp_code:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.info(request, '2 دقیقه منتظر بمانید')
                    return redirect(request.META.get('HTTP_REFERER'))
            except:
                pass
        else:
            pass

    return wrapped_view
