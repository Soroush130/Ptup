from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps
import re

from ptup_messages.models import Message


def is_receiver_or_sender(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        user = request.user
        url = request.get_full_path()
        match = re.search(r'/detail/(\d+)/', url)

        if match:
            message_id = int(match.group(1))
            message = Message.objects.get(id=message_id)
            if user == message.receiver or user == message.sender:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "شما اجازه دیدن این پیام را ندارید")
                return redirect('ptup_messages:messages')

    return wrapped_view
