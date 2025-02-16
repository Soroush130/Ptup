from django.db import models

from accounts.models import User
from customers.models import Customer
from doctors.models import Doctor


class Question(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='مراجع')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='درمانگر')
    question_text = models.TextField(verbose_name='متن سوال :')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد سوال')

    class Meta:
        db_table = 'questions'
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='سوال')
    answer_text = models.TextField(verbose_name='جواب سوال :')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد پاسخ')

    class Meta:
        db_table = 'Answers'
        verbose_name = 'پاسخ'
        verbose_name_plural = 'پاسخ ها'