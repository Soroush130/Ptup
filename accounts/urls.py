from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/customer/', views.register_page_customer, name='register_customer'),
    path('register/doctor/', views.register_page_doctor, name='register_doctor'),
    path('logout/', views.log_out, name='logout'),
]