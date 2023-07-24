from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps


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