from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('completion_information_doctor/', views.CompletionInformationDoctor.as_view(),
         name='completion_information_doctor'),
    path('get_identification_document_doctor/', views.GetIdentificationDocumentDoctor.as_view(),
         name='get_identification_document_doctor'),
    path('delete_document/<int:pk>/', views.DeleteIdentificationDocument.as_view(),
         name='delete_document'),
    path('list_customers_requested/', views.ListCustomerEachDoctor.as_view(), name="list_customers_requested"),
]
