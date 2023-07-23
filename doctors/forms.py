from django import forms
from .models import Doctor, IdentificationDocument


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = (
            'first_name',
            'last_name',
            'email',
            'gender',
            'home_address',
            'clinic_address',
            'home_number',
            'national_code',
            'psychology_license_number',
            'university_graduate',
            'field_of_study_bachelor',
            'field_of_study_residence',
            'city_of_residence',
            'treatment_history',
            'approach_used_treatment',
            'image_profile',
        )


class IdentificationDocumentForm(forms.ModelForm):
    title = forms.CharField(error_messages={
        'required': "عنوان باید وارد شود",
    })
    file = forms.FileField(widget=forms.FileInput, error_messages={
        'required': "فایل باید وارد شود",
    })

    class Meta:
        model = IdentificationDocument
        fields = ('title', 'file')


class NickNameForm(forms.Form):
    customer_id = forms.IntegerField(widget=forms.HiddenInput)
    nick_name = forms.CharField()


# class ConfirmationDoctorForm(forms.Form):
#     doctor_id = forms.IntegerField(widget=forms.HiddenInput)
#     is_verify = forms.BooleanField()
