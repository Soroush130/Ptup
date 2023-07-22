from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from doctors.decorators import is_complete_information_doctor
from doctors.utility import check_information_doctor


@login_required(login_url='accounts:login')
@is_complete_information_doctor
def home(request):
    return render(request, 'index.html', {})


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
