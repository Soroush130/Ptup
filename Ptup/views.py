from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from doctors.decorators import is_complete_information
from doctors.utility import check_information_doctor
from ptup_utilities.utility import get_context_according_user_role


@login_required(login_url='accounts:login')
@is_complete_information
def home(request):
    _URL = request.META.get("HTTP_REFERER")
    user = request.user
    role = user.role
    DOCTOR = 1
    _template_name = 'home_doctor.html' if role == DOCTOR else 'home_customer.html'
    context = get_context_according_user_role(roll_back_url=_URL, user=user, user_role=role)
    return render(request, _template_name, context)


def header(request):
    user = request.user
    user_role = user.role
    is_complete_information_doctor = check_information_doctor(user)
    context = {
        'user': user,
        'user_role': user_role,
        'is_complete_information_doctor': is_complete_information_doctor,
    }
    return render(request, 'shared/Header.html', context)


def footer(request):
    return render(request, 'shared/Footer.html', {})
