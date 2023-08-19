from django.contrib import admin

from .models import (
    HealingContent,
    HealingDay,
    DayFeedback,
    QuestionnaireWeek,
    QuestionWeek,
    QuestionOptionWeek,
    QuestionnaireWeekAnswer,
    QuestionnaireWeekAnswerDetail
)


class HealingContentAdmin(admin.ModelAdmin):
    list_display = ['healing_day', 'type']


class QuestionOptionWeekInline(admin.TabularInline):
    model = QuestionOptionWeek


class QuestionWeekAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionWeekInline]


admin.site.register(HealingDay)
admin.site.register(HealingContent, HealingContentAdmin)
admin.site.register(DayFeedback)

admin.site.register(QuestionnaireWeek)
admin.site.register(QuestionWeek, QuestionWeekAdmin)
admin.site.register(QuestionOptionWeek)

admin.site.register(QuestionnaireWeekAnswer)
admin.site.register(QuestionnaireWeekAnswerDetail)
