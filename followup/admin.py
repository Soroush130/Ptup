from django.contrib import admin

from followup.models import FollowUpQuestion, FollowUpQuestionAnswer


class FollowUpQuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'score', 'answer_date', 'question']


admin.site.register(FollowUpQuestion)

admin.site.register(FollowUpQuestionAnswer, FollowUpQuestionAnswerAdmin)
