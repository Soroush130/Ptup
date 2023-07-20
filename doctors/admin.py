from django.contrib import admin
from .models import Doctor, IdentificationDocument, ApproachUsedTreatment

admin.site.register(Doctor)
admin.site.register(IdentificationDocument)
admin.site.register(ApproachUsedTreatment)
