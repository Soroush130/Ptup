from django.contrib import admin
from .models import Customer, CustomerDiseaseInformation

admin.site.register(Customer)

admin.site.register(CustomerDiseaseInformation)