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


class PermissionStartTreatmentCustomerForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)
    permission_start_treatment = forms.CharField()

class CustomerIllnessForm(forms.Form):
    illness_id = forms.IntegerField(widget=forms.HiddenInput)
    illness = forms.BooleanField()
