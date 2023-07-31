from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/customer/', views.register_page_customer, name='register_customer'),
    path('register/doctor/', views.register_page_doctor, name='register_doctor'),
    path('confirm_otp/', views.ConfirmOtpCodeView.as_view(), name='confirm_otp'),
    path('logout/', views.log_out, name='logout'),

    path('confirm_doctor/', views.ConfirmationDoctorByStaff.as_view(), name='confirm_doctor'),
]