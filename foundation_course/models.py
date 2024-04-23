from django.db import models

from django_quill.fields import QuillField

from customers.models import Customer
from foundation_course.interpretation.interpretation import (
    interpretation_bai,
    interpretation_bdi,
    interpretation_ders,
    interpretation_qli,
    interpretation_medi,
    interpretation_neo
)


class QuestionnaireTypeChoices(models.IntegerChoices):
    BAI = 1, 'bai'
    BDI = 2, 'bdi'
    DERS = 3, 'ders'
    QLI = 4, 'qli'
    NEO = 5, 'neo'
    BEAQ = 6, 'beaq'
    MEDI = 7, 'medi'


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
    type = models.PositiveSmallIntegerField(
        verbose_name='نوع پرسشنامه',
        null=True,
        blank=True,
        choices=QuestionnaireTypeChoices.choices
    )
    dependency = models.ForeignKey(
        'self',
        related_name='dependencies',
        on_delete=models.CASCADE,
        verbose_name='وابستگی',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'questionnaire'
        verbose_name = 'پرسشنامه'
        verbose_name_plural = 'پرسشنامه های دوره مقدماتی'

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
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات دوره مقدماتی'


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
        verbose_name = 'گزینه'
        verbose_name_plural = 'گزینه های سوالات دوره مقدماتی'

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
        verbose_name = 'جواب'
        verbose_name_plural = 'جواب سوالات دوره مقدماتی'

    def __str__(self):
        return f'{self.pk} of question {self.questionnaire.pk}'

    @property
    def questionnaire_interpretation(self):
        questionnaire_type = self.questionnaire.get_type_display()

        if questionnaire_type == 'bai':
            interpretation = interpretation_bai(self.score)
            return interpretation

        elif questionnaire_type == 'bdi':
            # question_suicide_row = 9
            # check_suicide(question_suicide_row, self.id, self.customer)

            interpretation = interpretation_bdi(self.score)
            return interpretation

        elif questionnaire_type == 'ders':
            interpretation = interpretation_ders(self.score, self.id)
            return interpretation

        elif questionnaire_type == "qli" and self.questionnaire.dependency is not None:
            interpretation = interpretation_qli(self.score, self.id, self.questionnaire)
            return interpretation

        elif questionnaire_type == 'medi':
            interpretation = interpretation_medi(self.score, self.id)
            return interpretation

        elif questionnaire_type == 'neo':
            interpretation = interpretation_neo(self.id)
            return interpretation
        else:
            pass


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
        verbose_name = 'جزییات جواب'
        verbose_name_plural = 'جزییات جواب های دوره مقدماتی'

    def __str__(self):
        return f'{self.pk}'
