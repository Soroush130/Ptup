from django import forms

from customers.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            'age',
            'gender',
            'treating_doctor',
        )


class CustomerIllnessForm(forms.Form):
    illness_id = forms.IntegerField(widget=forms.HiddenInput)
    illness = forms.BooleanField()
