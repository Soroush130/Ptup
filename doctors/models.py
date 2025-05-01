from django.db import models
from django.utils import timezone
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from kavenegar import *

from accounts.models import User
from accounts.utilites import phone_number_decryption


class GenderChoices(models.IntegerChoices):
    MEN = 1, 'مرد'
    WOMEN = 2, 'زن'


class ApproachUsedTreatment(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان ')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'رویکرد درمان'
        verbose_name_plural = 'رویکرد های درمان'


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر")
    first_name = models.CharField(max_length=255, verbose_name='نام')
    last_name = models.CharField(max_length=255, verbose_name='نام خانوادگی')
    email = models.EmailField(verbose_name='ایمیل')
    gender = models.SmallIntegerField(choices=GenderChoices.choices, default=GenderChoices.MEN, verbose_name='جنسیت')
    home_address = models.CharField(max_length=550, verbose_name='آدرس خانه')
    clinic_address = models.CharField(max_length=550, verbose_name='آدرس کلنیک')
    home_number = models.CharField(max_length=30, verbose_name='شماره تلفن خانه')
    national_code = models.CharField(max_length=20, verbose_name='کد ملی')
    psychology_license_number = models.CharField(max_length=100, verbose_name='شماره پروانه نظام روانشناسی')
    university_graduate = models.CharField(max_length=255, verbose_name='دانشگاه فارغ التحصیلی')
    field_of_study_bachelor = models.CharField(max_length=255, verbose_name='رشته تحصیلی لیسانس')
    field_of_study_residence = models.CharField(max_length=255, verbose_name='رشته تحصیلی ارشد')
    city_of_residence = models.CharField(max_length=255, verbose_name='شهر محل اقامت')
    treatment_history = models.PositiveSmallIntegerField(default=0, verbose_name='سابقه درمانی')
    approach_used_treatment = models.ForeignKey(ApproachUsedTreatment, on_delete=models.SET_NULL, null=True, blank=True,
                                                verbose_name='رویکرد مورد استفاده در درمان ')
    image_profile = models.ImageField(upload_to='files/image_profile_doctors/', verbose_name='عکس')
    is_verify = models.BooleanField(default=False, verbose_name='اجازه شروع فعالیت')

    def __str__(self):
        return f"درمانگر {self.first_name} {self.last_name}"

    @property
    def get_full_name(self):
        return self.__str__()

    @property
    def get_image_profile_url(self):
        image_profile_url = self.image_profile.url
        if image_profile_url:
            return image_profile_url
        return ''

    @property
    def get_gender(self):
        return 'مرد' if self.gender == 1 else 'زن'

    class Meta:
        verbose_name = 'درمانگر'
        verbose_name_plural = 'لیست درمانگرها'


class IdentificationDocument(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='درمانگر ')
    title = models.CharField(max_length=255, verbose_name='عنوان فایل ')
    file = models.FileField(verbose_name='فایل ', upload_to='files/identification_document/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} : {self.doctor}"

    @property
    def get_file_size_as_str(self):
        file_size_bytes = self.file.size
        # Define the size units and their corresponding labels
        size_units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        index = 0

        while file_size_bytes >= 1024 and index < len(size_units) - 1:
            file_size_bytes /= 1024
            index += 1

        return f"{file_size_bytes:.2f} {size_units[index]}"

    class Meta:
        verbose_name = 'مدرک شناسایی'
        verbose_name_plural = 'مدارک شناسایی درمانگرها'


class SendSms(models.Model):
    customers = models.ManyToManyField('customers.Customer', verbose_name='لیست مراجع')
    message = models.TextField(verbose_name='متن پیام')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'پیامک'
        verbose_name_plural = 'پیامک ها'

class SmsSendError(models.Model):
    nick_name = models.CharField(max_length=255, verbose_name="نام مستعار")
    phone = models.CharField(max_length=20, verbose_name="شماره تلفن")
    message_text = models.TextField(verbose_name="متن پیامک")
    error_message = models.TextField(verbose_name="پیام خطا")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    def __str__(self):
        return f"{self.nick_name} - {self.phone}"


@receiver(m2m_changed, sender=SendSms.customers.through)
def send_sms_by_doctor_to_customers(sender, instance, action, **kwargs):
    from customers.models import Customer
    api_key = '4B7A74474B48663357344144706B2B3656594E553459484B566A56517857664C746F6F6D7655346F434C633D'
    Sender_Phone = '9982002631'

    if action == 'post_add':
        api = KavenegarAPI(api_key)
        for customer in instance.customers.all():

            if customer.user.phone.isdigit():
                receptor = customer.user.phone
            else:
                receptor = phone_number_decryption(phone_number=customer.user.phone)

            try:
                params = {
                    'sender': Sender_Phone,
                    'receptor': receptor,
                    'message': instance.message,
                }
                api.sms_send(params)
            except (APIException, HTTPException, Exception) as e:
                SmsSendError.objects.create(
                    nick_name=customer.nick_name,
                    phone=customer.user.phone,
                    message_text=instance.message,
                    error_message=str(e),
                )

