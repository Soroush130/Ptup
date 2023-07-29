from django.db import models


class Illness(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان بیماری')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')

    def __str__(self):
        return self.title
