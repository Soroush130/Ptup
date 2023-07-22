from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from doctors.decorators import is_complete_information_doctor
from doctors.utility import check_information_doctor


@login_required(login_url='accounts:login')
@is_complete_information_doctor
def home(request):
    role = request.user.role
    DOCTOR = 1
    _template_name = 'home_doctor.html' if role == DOCTOR else 'home_customer.html'
    print(_template_name)
    return render(request, _template_name, {})


def header(request):
    user = request.user
    user_role = user.role
    is_complete_information = check_information_doctor(user)
    context = {
        'user_role': user_role,
        'is_complete_information': is_complete_information,
    }
    return render(request, 'shared/Header.html', context)


def footer(request):
    return render(request, 'shared/Footer.html', {})
