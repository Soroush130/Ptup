from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('completion_information_customer/', views.CompletionInformationCostumer.as_view(),
         name='completion_information_customer'),

    path('filter_customer/', views.FilterCustomer.as_view(), name="filter_customer"),
]
