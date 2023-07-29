from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('completion_information_customer/', views.CompletionInformationCostumer.as_view(),
         name='completion_information_customer'),

    path('filter_customer/', views.FilterCustomer.as_view(), name="filter_customer"),
    path('determining_customer_illness/<int:customer_id>/', views.DeterminingCustomerIllness.as_view(),
         name="determining_customer_illness"),

    path('operation_choice_illness_customer/<int:customer_id>/<int:illness_id>/',
         views.OperationChoiceIllnessCustomer.as_view(),
         name="operation_choice_illness_customer"),
]
