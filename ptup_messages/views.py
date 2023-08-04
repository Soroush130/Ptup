from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from ptup_messages.models import Message
from ptup_messages.utility import read_message


class MessagesView(View):
    context = {}

    def get(self, request, *args, **kwargs):
        param = request.GET.get('type', 'inbox')
        if param == "inbox":
            list_messages = Message.objects.filter(receiver=request.user)
            self.context['list_messages'] = list_messages
        elif param == "sent":
            list_messages = Message.objects.filter(sender=request.user)
            self.context['list_messages'] = list_messages
        elif param == "read":
            list_messages = Message.objects.filter(receiver=request.user, is_read=True)
            self.context['list_messages'] = list_messages
        else:
            list_messages = Message.objects.filter(receiver=request.user, is_read=False)
            self.context['list_messages'] = list_messages

        return render(request, 'ptup_messages/messages.html', self.context)


class DetailMessageView(View):
    def get(self, request, message_id, *args, **kwargs):
        message = Message.objects.get(id=message_id)

        read_message(message)

        context = {
            "message": message,
        }
        return render(request, 'ptup_messages/message_detail.html', context)


class DeleteMessageView(View):
    def get(self, request, message_id, *args, **kwargs):
        Message.objects.get(id=message_id).delete()
        messages.success(request, "پیام با موفقیت حذف شد")
        return redirect('ptup_messages:messages')
