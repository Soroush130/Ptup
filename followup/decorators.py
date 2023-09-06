from datetime import datetime
from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def after_nine_pm(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        current_time = datetime.now().time()
        nine_pm = datetime.strptime("21:00:00", "%H:%M:%S").time()
        twelve_pm = datetime.strptime("23:59:59", "%H:%M:%S").time()

        if current_time >= nine_pm and current_time <= twelve_pm:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "زمان پاسخگویی دوره فالوآپ از ساعت 9 شب تا 12 شب است")
            return redirect('home')

    return wrapped_view
