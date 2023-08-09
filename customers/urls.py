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

    path('permission_start_treatment/', views.PermissionStartTreatmentCustomer.as_view(),
         name='permission_start_treatment'),

    path('healing_period_customer/', views.HealingPeriodCustomer.as_view(), name='healing_period_customer'),

    path('foundation_course_customer/', views.FoundationCourseCustomer.as_view(), name='foundation_course_customer'),

    path('follow_up_customer/', views.FollowUpCustomer.as_view(), name='follow_up_customer'),
]
