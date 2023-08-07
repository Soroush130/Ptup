from django import forms
from ptup_messages.models import Message
from django_quill.forms import QuillFormField


class MessageForm(forms.Form):
    receiver = forms.CharField()
    subject = forms.CharField()
    content = QuillFormField()
