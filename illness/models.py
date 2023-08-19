from django.db import models


class Illness(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان بیماری')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')

    def __str__(self):
        return self.title


class HealingPeriod(models.Model):
    illness = models.OneToOneField(Illness, on_delete=models.CASCADE, verbose_name="بیماری ")
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name="عنوان دوره درمان ")
    duration_of_treatment = models.PositiveIntegerField(verbose_name="طول دروه درمان ", help_text="بر اساس تعداد هفته ")

    def __str__(self):
        return f"{self.title}"
