from django.db import models

from django_quill.fields import QuillField

from customers.models import Customer


class Questionnaire(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='عنوان'
    )
    description = QuillField(
        verbose_name='توضیحات'
    )
    number_of_options = models.PositiveIntegerField(
        verbose_name='تعداد گزینه',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'questionnaire'

    def __str__(self):
        return self.title


class Question(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire,
        related_name='questions',
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
        db_table = 'question'

    def __str__(self):
        return f'{self.pk} of {self.questionnaire.title}'


class QuestionOption(models.Model):
    question = models.ForeignKey(
        Question,
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
        db_table = 'question_option'

    def __str__(self):
        return f'{self.pk} of question {self.question.pk}'


#  ===================================================================


class QuestionnaireAnswer(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire,
        related_name='questionnaire_answer',
        on_delete=models.PROTECT,
        verbose_name='پرسشنامه'
    )
    customer = models.ForeignKey(
        Customer,
        verbose_name='بیمار',
        related_name='questionnaire_answer_customer',
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
        db_table = 'questionnaire_answer'

    def __str__(self):
        return f'{self.pk} of question {self.questionnaire.pk}'


class QuestionnaireAnswerDetail(models.Model):
    questionnaire_answer = models.ForeignKey(
        QuestionnaireAnswer,
        verbose_name='جواب پرسشنامه',
        related_name='questionnaire_answer_detail',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        related_name='question_answer_option',
        on_delete=models.CASCADE,
        verbose_name='سوال'
    )
    question_option = models.ForeignKey(
        QuestionOption,
        related_name='question_option_answer_option',
        on_delete=models.CASCADE,
        verbose_name='جواب سوال'
    )

    class Meta:
        db_table = 'question_answer_detail'

    def __str__(self):
        return f'{self.pk}'
