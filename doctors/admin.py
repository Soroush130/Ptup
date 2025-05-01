from django.contrib import admin
from .models import Doctor, IdentificationDocument, ApproachUsedTreatment, SendSms, SmsSendError

admin.site.register(Doctor)
admin.site.register(IdentificationDocument)
admin.site.register(ApproachUsedTreatment)


class SendSmsAdmin(admin.ModelAdmin):
    list_display = (
        "message",
        "created_at",
    )


admin.site.register(SendSms, SendSmsAdmin)


class SmsSendErrorAdmin(admin.ModelAdmin):
    list_display = [
        'nick_name',
        'phone',
        'error_message'
    ]
admin.site.register(SmsSendError, SmsSendErrorAdmin)
