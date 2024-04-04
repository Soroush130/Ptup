from django.contrib import admin

from customers.models import CustomerDiseaseInformation
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
    list_display = [
        "questionnaire",
        "row",
        "text",
    ]


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'dependency']


class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = [
        'question',
        'coefficient',
        'text',
        'row',
    ]


admin.site.register(Questionnaire, QuestionnaireAdmin)

admin.site.register(Question, QuestionAdmin)

admin.site.register(QuestionOption, QuestionOptionAdmin)


class QuestionnaireAnswerAdmin(admin.ModelAdmin):
    list_display = ['questionnaire', 'customer', 'answer_time', 'score']
    model = QuestionnaireAnswer
    actions = ['delete_selected']

    def delete_queryset(self, request, queryset):

        for obj in queryset:
            customer = obj.customer
            disease_information = CustomerDiseaseInformation.objects.filter(
                customer=customer,
                is_finished=False
            ).first()

            if disease_information.is_foundation_course:
                disease_information.is_foundation_course = False
                disease_information.save()

                obj.delete()
            else:
                obj.delete()


class QuestionnaireAnswerDetailAdmin(admin.ModelAdmin):
    list_display = [
        "questionnaire_answer",
        "question",
        "question_option",
    ]


admin.site.register(QuestionnaireAnswer, QuestionnaireAnswerAdmin)

admin.site.register(QuestionnaireAnswerDetail, QuestionnaireAnswerDetailAdmin)
