from django import forms
from django.core.exceptions import ValidationError
from django_quill.forms import QuillFormField


def validate_receiver(text):
    if not text.isnumeric():
        raise ValidationError('فیلد گیرنده فقط باید عدد باشد')


class MessageForm(forms.Form):
    receiver = forms.CharField(validators=[validate_receiver])
    subject = forms.CharField()
    content = QuillFormField()
    file = forms.FileField(widget=forms.FileInput)
