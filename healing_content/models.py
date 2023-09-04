from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from customers.models import Customer
from doctors.models import Doctor
from illness.models import Illness, HealingPeriod



class HealingWeek(models.Model):
    healing_period = models.ForeignKey(HealingPeriod, on_delete=models.CASCADE, verbose_name='دوره درمانی ')
    week = models.PositiveIntegerField(default=1, verbose_name='شماره هفته', help_text='هفته چندم از دوره درمانی')

    class Meta:
        db_table = 'healing_week'

    def __str__(self):
        return f"هفته {self.week} از دوره درمان {self.healing_period} || {self.pk}"

    def clean(self):
        healing_week = HealingWeek.objects.filter(healing_period=self.healing_period, week=self.week)
        if healing_week.exists():
            raise ValidationError("چنین هفته ای وجود دارد")


class HealingContent(models.Model):
    TYPE_HEALING_CONTENT = (
        ('MEDIA', 'ویدیو'),
        ('FILE', 'فایل'),
        ('VOICE', 'صدا'),
    )
    healing_week = models.ForeignKey(HealingWeek, on_delete=models.CASCADE, verbose_name='هفته چندم ')
    # title =
    type = models.CharField(max_length=8, choices=TYPE_HEALING_CONTENT)
    # This field is mostly used to group content
    day = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=1,
        verbose_name='روز هفته',
        validators=[
            MinValueValidator(1, message='نباید کمتر از 1 باشید'),
            MaxValueValidator(7, message='نباید بیشتر از 7 باشد')
        ]
    )
    file = models.FileField(upload_to='healing_content/media_practice/', verbose_name='فایل ')

    class Meta:
        db_table = 'healing_content'


class Practice(models.Model):
    healing_week = models.ForeignKey(HealingWeek, on_delete=models.CASCADE, verbose_name='هفته چندم ')
    description = models.TextField(verbose_name='توضیحات')

    class Meta:
        db_table = 'practice'

    def __str__(self):
        return f"Practice with ID #{self.pk}"


class QuestionPractice(models.Model):
    practice = models.ForeignKey(
        Practice,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name='تمرین '
    )
    row = models.PositiveIntegerField(
        verbose_name='شماره سوال',
    )
    text = models.TextField(
        verbose_name='متن سوال'
    )

    class Meta:
        db_table = 'question_practice'


class AnswerPractice(models.Model):
    healing_week = models.ForeignKey(
        HealingWeek,
        on_delete=models.CASCADE,
        verbose_name='هفته چندم '
    )
    question_practice = models.ForeignKey(
        QuestionPractice,
        on_delete=models.CASCADE,
        related_name='answer_practice',
        verbose_name='سوال'
    )
    answer = models.TextField(
        verbose_name='جواب'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='customer_answer_practice',
        verbose_name='مراجع'
    )
    time_answer = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان پاسخ'
    )

    class Meta:
        db_table = 'answer_practices'


# =========================================== Questionnaire Week ==========================
class QuestionnaireWeek(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='عنوان'
    )
    description = models.TextField(
        verbose_name='توضیحات'
    )
    number_of_options = models.PositiveIntegerField(
        verbose_name='تعداد گزینه',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'questionnaire_week'

    def __str__(self):
        return self.title


class QuestionWeek(models.Model):
    questionnaire_week = models.ForeignKey(
        QuestionnaireWeek,
        related_name='week_questions',
        on_delete=models.CASCADE,
        verbose_name='پرسشنامه'
    )
    row = models.PositiveIntegerField(
        verbose_name='شماره سوال',
    )
    text = models.TextField(
        verbose_name='متن سوال'
    )

    class Meta:
        db_table = 'question_week'


class QuestionOptionWeek(models.Model):
    question_week = models.ForeignKey(
        QuestionWeek,
        related_name='question_option',
        on_delete=models.CASCADE,
        verbose_name='سوال'
    )
    coefficient = models.IntegerField(
        verbose_name='ضریب گزینه'
    )
    text = models.TextField(
        verbose_name='متن گزینه'
    )
    row = models.PositiveIntegerField(
        verbose_name='شماره گزینه'
    )

    class Meta:
        db_table = 'question_option_week'


# ------------------------  Question Answer --------------

class QuestionnaireWeekAnswer(models.Model):
    questionnaire_week = models.ForeignKey(
        QuestionnaireWeek,
        related_name='questionnaire_week_answer',
        on_delete=models.PROTECT,
        verbose_name='پرسشنامه'
    )
    healing_week = models.ForeignKey(
        HealingWeek,
        on_delete=models.CASCADE,
        related_name='day_questionnaire_week_answer',
        verbose_name='هفتههفته',
        help_text='برای کدام هفته و گدام دوره درمان است'
    )
    customer = models.ForeignKey(
        Customer,
        verbose_name='بیمار',
        related_name='customer_questionnaire_answer',
        on_delete=models.CASCADE
    )

    answer_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان پاسخگویی'
    )

    score = models.FloatField(
        verbose_name='امتیاز',
        default=0.00
    )

    class Meta:
        db_table = 'questionnaire_week_answers'


class QuestionnaireWeekAnswerDetail(models.Model):
    questionnaire_week = models.ForeignKey(
        QuestionnaireWeekAnswer,
        verbose_name='جواب پرسشنامه',
        related_name='questionnaire_week_answer_detail',
        on_delete=models.CASCADE
    )
    question_week = models.ForeignKey(
        QuestionWeek,
        related_name='question_week_answer_option',
        on_delete=models.CASCADE,
        verbose_name='سوال'
    )
    question_option_week = models.ForeignKey(
        QuestionOptionWeek,
        related_name='question_option_week_answer_option',
        on_delete=models.CASCADE,
        verbose_name='جواب سوال'
    )

    class Meta:
        db_table = 'questionnaire_week_answer_details'

    def __str__(self):
        return f'{self.pk}'


# ======================================  Day Feedback   ======================
class DayFeedback(models.Model):
    practice_answer = models.ForeignKey(
        AnswerPractice,
        on_delete=models.CASCADE,
        related_name='dey_feedbacks',
        verbose_name='تمرین',
        help_text='برای کدام تمرین است'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name='دکتر',
        related_name='doctor_day_feedbacks'
    )
    subject = models.CharField(
        max_length=255,
        verbose_name='عنوان'
    )
    content = models.TextField(
        verbose_name='توضیحات'
    )

    class Meta:
        db_table = 'day_feedback'

    def __str__(self):
        return self.subject
