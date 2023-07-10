from django.shortcuts import render


def home(request):
    return render(request, 'index.html', {})


def header(request):
    return render(request, 'shared/Header.html', {})


def footer(request):
    return render(request, 'shared/Footer.html', {})