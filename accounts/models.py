from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone, role, password=None):
        if not phone:
            raise ValueError('شماره تلفن ضروری است')

        user = self.model(phone=phone, role=role)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, role, password=None):
        user = self.create_user(
            phone=phone,
            role=role,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class RoleChoices(models.IntegerChoices):
    ADMIN = 0, 'ادمین'
    DOCTER = 1, 'دکتر'
    CUSTOMER = 2, 'بیمار'


class User(AbstractBaseUser):
    phone = models.CharField(verbose_name="شماره تلفن", max_length=21, unique=True)
    role = models.SmallIntegerField(verbose_name="نقش", default=None, null=True, choices=RoleChoices.choices)
    is_accept_rules = models.BooleanField(verbose_name="پذیرش قوانین سایت", default=False)
    is_active = models.BooleanField(verbose_name="فعال", default=True)
    is_staff = models.BooleanField(verbose_name="کارمند", default=False)
    is_superuser = models.BooleanField(verbose_name="ادمین", default=False)
    data_joined = models.DateTimeField(verbose_name="تاریخ عضویت", null=True)
    last_login = models.DateTimeField(verbose_name="اخرین زمان لاگین", null=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.is_staff


class SiteRules(models.Model):
    rule = models.CharField(max_length=300, verbose_name='قانون')

    def __str__(self):
        return self.rule
