from django.db import models


class Guide(models.Model):
    FILE_TYPE = (
        ('file', 'فایل'),
        ('video', 'ویدیو')
    )
    type = models.CharField(
        max_length=10,
        verbose_name='نوع فایل ',
        choices=FILE_TYPE
    )
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
        verbose_name = 'راهنما'
        verbose_name_plural = 'راهنما ها'
        db_table = 'guide'
