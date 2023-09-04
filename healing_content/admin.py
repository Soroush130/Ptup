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

admin.site.register(QuestionnaireWeekAnswer)
admin.site.register(QuestionnaireWeekAnswerDetail)


# ====================== Old models practice ===============
# class PracticeAnswerDetailInline(admin.TabularInline):
#     model = PracticeAnswerDetail
#
#
# class PracticeAnswerAdmin(admin.ModelAdmin):
#     inlines = [PracticeAnswerDetailInline]
#
#
# admin.site.register(PracticeAnswer, PracticeAnswerAdmin)
# admin.site.register(PracticeAnswerDetail)
# ===========================================================

# ======================= New models practice =================
admin.site.register(Practice)
admin.site.register(QuestionPractice)
admin.site.register(AnswerPractice)
# ===========================================================