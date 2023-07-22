from django.db import models
from accounts.models import User


class GenderChoices(models.IntegerChoices):
    MEN = 1, 'مرد'
    WOMEN = 2, 'زن'


class ApproachUsedTreatment(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان ')

    def __str__(self):
        return self.title


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
    is_verify = models.BooleanField(default=False, verbose_name='اجازه شروع فعالیت')

    def __str__(self):
        return f"دکتر {self.first_name} {self.last_name}"

    @property
    def get_full_name(self):
        return self.__str__()


class IdentificationDocument(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='دکتر ')
    title = models.CharField(max_length=255, verbose_name='عنوان فایل ')
    file = models.FileField(verbose_name='فایل ')

    def __str__(self):
        return f"{self.title} : {self.doctor}"
