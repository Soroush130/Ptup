from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('completion_information_customer/', views.CompletionInformationCostumer.as_view(),
         name='completion_information_customer'),

    path('filter_customer/', views.FilterCustomer.as_view(), name="filter_customer"),

    path('customer/<int:customer_id>/detail/', views.CustomerInformationDetail.as_view(), name="customer_detail"),

    path('determining_customer_illness/<int:customer_id>/', views.DeterminingCustomerIllness.as_view(),
         name="determining_customer_illness"),

    path('operation_choice_illness_customer/<int:customer_id>/<int:illness_id>/',
         views.OperationChoiceIllnessCustomer.as_view(),
         name="operation_choice_illness_customer"),

    path('permission_start_treatment/', views.PermissionStartTreatmentCustomer.as_view(),
         name='permission_start_treatment'),

    # --------------------------------------------------

    path('healing_period_each_week/', views.healing_content_each_week, name='healing_period_each_week'),

    path('practices_each_week/<int:practice_each_week_id>/', views.practice_each_week,
         name='practices_each_week'),

    path('questionnaires_weekly/', views.questionnaires_weekly, name='questionnaires_weekly'),

    path('healing_content_map/', views.HealingContentMap.as_view(), name="healing_content_map"),

    path('completion_practice/', views.CompletionPractice.as_view(), name='completion_practice'),

    path('foundation_course_customer/', views.FoundationCourseCustomer.as_view(), name='foundation_course_customer'),

]
