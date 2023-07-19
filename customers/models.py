from django.db import models
from accounts.models import User


class GenderChoices(models.IntegerChoices):
    MEN = 1, 'مرد'
    WOMEN = 2, 'زن'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر")
    nick_name = models.CharField(verbose_name="نام مستعار", max_length=255)
    age = models.PositiveIntegerField(default=0, verbose_name='سن')
    gender = models.SmallIntegerField(choices=GenderChoices.choices, default=GenderChoices.MEN, verbose_name='جنسیت')
    # treating_doctor
    permission_start_treatment = models.BooleanField(default=False, verbose_name='اجازه شروع دوره درمان')

    def __str__(self):
        return f"{self.user} : {self.nick_name}"

