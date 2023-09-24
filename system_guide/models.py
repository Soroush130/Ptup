from django.db import models


class Guide(models.Model):
    title = models.CharField(
        verbose_name='عنوان ',
        blank=True,
        null=True
    )
    file = models.FileField(
        upload_to='system_guide/',
        verbose_name=' فایل راهنما '
    )

    class Meta:
        db_table = 'guide'
