from django import forms

from ptup_messages.models import Message


class MessageForm(forms.Form):
    receiver = forms.CharField()
    subject = forms.CharField()
    content = forms.CharField(widget=forms.TextInput)
