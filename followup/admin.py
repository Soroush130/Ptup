from django.contrib import admin

from followup.models import FollowUpQuestion, FollowUpQuestionAnswer, FollowUpContent


class FollowUpQuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'score', 'answer_date', 'day', 'question']
    list_filter = ['question']


admin.site.register(FollowUpQuestion)

admin.site.register(FollowUpQuestionAnswer, FollowUpQuestionAnswerAdmin)

admin.site.register(FollowUpContent)
