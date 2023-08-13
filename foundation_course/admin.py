from django.contrib import admin
from .models import (
    Questionnaire,
    Question,
    QuestionOption,
    QuestionnaireAnswer,
    QuestionnaireAnswerDetail
)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]


admin.site.register(Questionnaire)

admin.site.register(Question, QuestionAdmin)

admin.site.register(QuestionOption)

admin.site.register(QuestionnaireAnswer)

admin.site.register(QuestionnaireAnswerDetail)
