from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from customers.models import Customer


class FollowUpQuestion(models.Model):
    STRUCTURE_EVALUATED = (
        ('S', 'غمگینی'),
        ('A', 'اضطراب'),
        ('AN', 'خشم'),
        ('H', 'شادی'),
        ('AC', 'سطح فعالیت'),
        ('GE', 'آشنایی با نقش هیجان ها'),
        ('AT', 'توجه آگاهی'),
        ('CO', 'انعطاف شناختی'),
        ('TO', 'تحمل احساس های ناخوشایند جسمی'),
        ('NEB', 'رفتارهای غیر هیجانی - رفتارهایی که توسط هیجان ها هدایت نمی شوند'),
    )
    row = models.PositiveIntegerField(
        verbose_name='ردیف '
    )
    text = models.TextField(
        verbose_name='متن سوال '
    )
    structure_evaluated = models.CharField(
        max_length=5,
        verbose_name='سازه مورد ارزیابی ',
        choices=STRUCTURE_EVALUATED
    )
    description = models.TextField(
        verbose_name='راهنمایی سوال '
    )

    class Meta:
        db_table = 'follow_up_question'

    def __str__(self):
        return f"{self.row}"


class FollowUpQuestionAnswer(models.Model):
    question = models.ForeignKey(
        FollowUpQuestion,
        related_name='answers',
        verbose_name='سوال ',
        on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='answers_follow_up',
        verbose_name='کاربر '
    )
    day = models.PositiveSmallIntegerField(
        verbose_name='روز ',
        null=True,
        blank=True,
        default=1
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='امتیاز ',
        validators=[
            MinValueValidator(1, "حداقل نمره 1 است"),
            MaxValueValidator(10, "حداکثر نمره 10 است")
        ]
    )
    answer_date = models.DateField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'followup_question_answer'
