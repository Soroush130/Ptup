from django.contrib import admin
from .models import Customer, CustomerDiseaseInformation, CustomerActivityHistory

class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'get_user_phone',
        'nick_name'
    ]

    @admin.display(description='شماره تلفن')
    def get_user_phone(self, obj):
        return obj.user.phone

admin.site.register(Customer, CustomerAdmin)

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