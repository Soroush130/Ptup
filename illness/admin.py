from django.contrib import admin
from .models import Illness, HealingPeriod


admin.site.register(Illness)

admin.site.register(HealingPeriod)