from django.contrib import admin

from .models import (
    HealingContent,
    HealingWeek,
    DayFeedback,
    QuestionnaireWeek,
    QuestionWeek,
    QuestionOptionWeek,
    QuestionnaireWeekAnswer,
    QuestionnaireWeekAnswerDetail,
    # PracticeAnswer,
    # PracticeAnswerDetail,
    Practice,
    QuestionPractice,
    AnswerPractice,
    PracticeContent,
    HealingWeekViewLog,
)


class HealingContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'healing_week', 'type']


class QuestionOptionWeekInline(admin.TabularInline):
    model = QuestionOptionWeek


class QuestionWeekAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionWeekInline]


admin.site.register(HealingWeek)
admin.site.register(HealingContent, HealingContentAdmin)
admin.site.register(DayFeedback)

admin.site.register(QuestionnaireWeek)
admin.site.register(QuestionWeek, QuestionWeekAdmin)
admin.site.register(QuestionOptionWeek)


class QuestionnaireWeekAnswerAdmin(admin.ModelAdmin):
    list_display = [
        'questionnaire_week',
        'healing_week',
        'customer',
        'answer_time',
        'score',
    ]

    list_filter = ['customer']


admin.site.register(QuestionnaireWeekAnswer, QuestionnaireWeekAnswerAdmin)
admin.site.register(QuestionnaireWeekAnswerDetail)


# ======================= models practice =================
class PracticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'healing_week']


class PracticeContentAdmin(admin.ModelAdmin):
    list_display = ['practice', 'title', 'type', 'file']


admin.site.register(Practice, PracticeAdmin)
admin.site.register(PracticeContent, PracticeContentAdmin)
admin.site.register(QuestionPractice)


class AnswerPracticeAdmin(admin.ModelAdmin):
    list_display = [
        "healing_week",
        "practice",
        "answer",
        "file",
        "customer",
        "time_answer",
    ]


admin.site.register(AnswerPractice, AnswerPracticeAdmin)


# ===========================================================


@admin.register(HealingWeekViewLog)
class HealingWeekViewLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'healing_week', 'viewed_at')
    list_filter = ('healing_week__healing_period', 'user')
