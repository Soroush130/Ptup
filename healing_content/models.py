from django.core.exceptions import ValidationError
from django.db import models

from illness.models import Illness, HealingPeriod


class HealingContentBase(models.Model):
    TYPE_HEALING_CONTENT = (
        ('MEDIA', 'ویدیو'),
        ('PRACTICE', 'تمرین')
    )
    healing_period = models.ForeignKey(HealingPeriod, on_delete=models.CASCADE, verbose_name='دوره درمانی ')
    type = models.CharField(max_length=8, choices=TYPE_HEALING_CONTENT)

    class Meta:
        abstract = True


class Media(HealingContentBase):
    file = models.FileField(upload_to='healing_content/media_practice/', verbose_name='فایل ')
    day = models.PositiveIntegerField(default=1, verbose_name='شماره روز', help_text='روز چندم از دوره درمانی')

    def clean(self):
        super().clean()
        day = self.day

        total_days_in_healing_period = self.healing_period.duration_of_treatment * 7
        if day > total_days_in_healing_period:
            raise ValidationError("day more than total days in healing period")

        existing_day = Media.objects.filter(day=day, healing_period=self.healing_period)
        if existing_day.exists():
            raise ValidationError("برای این روز از دوره محتوا وجود دارد")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run full validation before saving
        return super().save(*args, **kwargs)


class Practice(HealingContentBase):
    # TODO: additional fields for this model
    day = models.PositiveIntegerField(default=1, verbose_name='شماره روز', help_text='روز چندم از دوره درمانی')

    def clean(self):
        super().clean()
        day = self.day

        total_days_in_healing_period = self.healing_period.duration_of_treatment * 7
        if day > total_days_in_healing_period:
            raise ValidationError("day more than total days in healing period")

        existing_day = Media.objects.filter(day=day, healing_period=self.healing_period)
        if existing_day.exists():
            raise ValidationError("برای این روز از دوره محتوا وجود دارد")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run full validation before saving
        return super().save(*args, **kwargs)