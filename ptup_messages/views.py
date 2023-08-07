from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from accounts.models import User
from ptup_messages.decorators import is_receiver_or_sender
from ptup_messages.forms import MessageForm
from ptup_messages.models import Message
from ptup_messages.utility import read_message


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
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


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
@method_decorator(is_receiver_or_sender, name='dispatch')
class DetailMessageView(View):
    def get(self, request, message_id, *args, **kwargs):
        message = Message.objects.get(id=message_id)

        if request.user == message.receiver:
            read_message(message)

        context = {
            "message": message,
        }
        return render(request, 'ptup_messages/message_detail.html', context)


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class DeleteMessageView(View):
    def get(self, request, message_id, *args, **kwargs):
        Message.objects.get(id=message_id).delete()
        messages.success(request, "پیام با موفقیت حذف شد")
        return redirect('ptup_messages:messages')


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class SendMessageView(View):
    def get(self, request):
        message_form = MessageForm()
        context = {
            "message_form": message_form,
        }
        return render(request, 'ptup_messages/send_message.html', context)

    def post(self, request):
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            phone = message_form.cleaned_data['receiver']
            try:
                receiver = User.objects.get(phone__exact=phone)
                subject = message_form.cleaned_data['subject']
                content = message_form.cleaned_data['content']
                Message.objects.create(
                    sender=request.user,
                    receiver=receiver,
                    subject=subject,
                    content=content
                )
                messages.success(request, "پیام شما ارسال شد")
                return redirect('ptup_messages:messages')
            except User.DoesNotExist:
                messages.error(request, "کاربر مورد نظر یافت نشد")
                return redirect('ptup_messages:send_messages')
        else:
            print(message_form.errors)
            return redirect('ptup_messages:send_messages')