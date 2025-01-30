from django.contrib import admin
from .models import Doctor, IdentificationDocument, ApproachUsedTreatment, SendSms

admin.site.register(Doctor)
admin.site.register(IdentificationDocument)
admin.site.register(ApproachUsedTreatment)


class SendSmsAdmin(admin.ModelAdmin):
    list_display = (
        "type_sms",
        "created_at",
    )


admin.site.register(SendSms, SendSmsAdmin)
