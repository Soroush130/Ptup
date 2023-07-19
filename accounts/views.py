from django.shortcuts import render


def login_page(request):
    context = {}
    return render(request, "accounts/login.html", context)


def register_page(request):
    context = {}
    return render(request, "accounts/register.html", context)


def log_out(request):
    pass
