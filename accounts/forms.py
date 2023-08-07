from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User
from django.db.models import Q

from .utilites import phone_number_encryption


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phone', 'role')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone', 'role')


class LoginUserForm(forms.Form):
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterCustomerForm(forms.Form):
    phone = forms.CharField()
    is_accept_rules = forms.BooleanField(error_messages={
        'required': "قوانین سایت باید پذیرفته شود",
    })
    password = forms.CharField(widget=forms.PasswordInput())
    re_password = forms.CharField(widget=forms.PasswordInput())

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')

        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')

        return password

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not phone.isdigit():
            raise forms.ValidationError("عدد وارد کنید")

        is_exists_phone = User.objects.filter(
            Q(phone__exact=phone) | Q(phone__exact=phone_number_encryption(phone))
        ).exists()
        if is_exists_phone:
            raise forms.ValidationError("چنین شماره تلفنی قبلا ثبت شده است")

        return phone


class RegisterDoctorForm(forms.Form):
    phone = forms.CharField()
    is_accept_rules = forms.BooleanField(error_messages={
        'required': "قوانین سایت باید پذیرفته شود",
    })
    password = forms.CharField(widget=forms.PasswordInput())
    re_password = forms.CharField(widget=forms.PasswordInput())

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')

        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')

        return password

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not phone.isdigit():
            raise forms.ValidationError("عدد وارد کنید")

        is_exists_phone = User.objects.filter(
            Q(phone__exact=phone) | Q(phone__exact=phone_number_encryption(phone))
        ).exists()
        if is_exists_phone:
            raise forms.ValidationError("چنین شماره تلفنی قبلا ثبت شده است")
        return phone


class OtpCodeForm(forms.Form):
    otp_code = forms.CharField()

    def clean_otp_code(self):
        otp_code = self.cleaned_data['otp_code']

        if not otp_code.isdigit():
            raise forms.ValidationError("عدد وارد کنید")

        if len(otp_code) > 5:
            raise forms.ValidationError("تعداد اعداد وارد شده بیشتر از حد مجاز است")
        elif len(otp_code) < 5:
            raise forms.ValidationError("تعداد اعداد وارد شده کمتر از حد مجاز است")
        else:
            pass

        return otp_code


class ForgotPasswordForm(forms.Form):
    phone = forms.CharField()

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not phone.isdigit():
            raise forms.ValidationError("عدد وارد کنید")

        is_exists_phone = User.objects.filter(
            Q(phone__exact=phone) | Q(phone__exact=phone_number_encryption(phone))
        ).exists()
        if not is_exists_phone:
            raise forms.ValidationError("چنین شماره تلفنی ثبت نشده است")
        return phone


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    re_password = forms.CharField(widget=forms.PasswordInput())

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')

        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')

        return password
