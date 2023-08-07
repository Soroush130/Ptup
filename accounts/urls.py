from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/customer/', views.register_page_customer, name='register_customer'),
    path('register/doctor/', views.register_page_doctor, name='register_doctor'),
    path('confirm_otp/', views.ConfirmOtpCodeView.as_view(), name='confirm_otp'),
    path('re_send_otp/', views.ReSendOtpCodeView.as_view(), name='re_send_otp'),
    path('logout/', views.log_out, name='logout'),
    #
    path('confirm_doctor/', views.ConfirmationDoctorByStaff.as_view(), name='confirm_doctor'),
    # Forgot Password
    path('forgot_password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('confirm_forgot_password/', views.ConfirmForgotPasswordView.as_view(), name='confirm_forgot_password'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
]