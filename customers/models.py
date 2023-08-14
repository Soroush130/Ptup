from django.db import models
from django.utils import timezone

from accounts.models import User
from accounts.utilites import phone_number_decryption
from doctors.models import Doctor
from illness.models import Illness, HealingPeriod


class GenderChoices(models.IntegerChoices):
    MEN = 1, 'مرد'
    WOMEN = 2, 'زن'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر")
    nick_name = models.CharField(verbose_name="نام مستعار", max_length=255, null=True, blank=True)
    age = models.PositiveIntegerField(default=0, verbose_name='سن')
    gender = models.SmallIntegerField(choices=GenderChoices.choices, default=GenderChoices.MEN, verbose_name='جنسیت')
    treating_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, verbose_name='دکتر معالج')
    permission_start_treatment = models.BooleanField(default=False, verbose_name='اجازه شروع دوره درمان')

    def __str__(self):
        return f"{self.user} : {self.nick_name} with id {self.id}"

    @property
    def phone(self):
        phone = self.user.phone
        phone = phone_number_decryption(phone)
        return phone

    @property
    def get_gender(self):
        return 'مرد' if self.gender == 1 else 'زن'


class CustomerDiseaseInformation(models.Model):
    """
        در این مدل اطلاعات بیماری مشتری ثبت خواهد شد
    """

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="بیمار "
    )
    illness = models.ForeignKey(
        Illness,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='بیماری '
    )
    healing_period = models.ForeignKey(
        HealingPeriod,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='دروه درومان ')
    day_of_healing_period = models.PositiveIntegerField(
        default=0,
        verbose_name='روز',
        help_text='روز چندم از دوره درمانی '
    )
    start_time_period = models.DateTimeField(
        verbose_name='زمان',
        help_text='زمان شروع دوره درمان ',
        null=True,
        blank=True
    )
    is_foundation_course = models.BooleanField(
        default=False,
        verbose_name='دوره مقدماتی',
        help_text='آیا دوره مقدماتی را سپری کرده است یا خیر'
    )
    is_healing_period = models.BooleanField(
        default=False,
        verbose_name='بله/خیر ',
        help_text='آیا دوره درمان را گذرانده است'
    )
    is_follow_up = models.BooleanField(
        default=False,
        verbose_name='دوره فالوآپ',
        help_text='آیا دوره فالوآپ را سپری کرده است یا خیر'
    )
    is_finished = models.BooleanField(
        default=False,
        verbose_name='اتمام',
        help_text='آیا این پرونده بسته شده است یا خیر'
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"{self.customer} , {self.illness} , {self.healing_period}"
