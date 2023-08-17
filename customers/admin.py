from django.contrib import admin
from .models import Customer, CustomerDiseaseInformation, CustomerActivityHistory

admin.site.register(Customer)

admin.site.register(CustomerDiseaseInformation)


class CustomerActivityHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'customer',
        'subject',
        'content',
        'created'
    ]
    search_fields = [
        'customer'
    ]


admin.site.register(CustomerActivityHistory, CustomerActivityHistoryAdmin)