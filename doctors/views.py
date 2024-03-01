from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator

from customers.models import Customer
from ptup_utilities.utility import send_notification_in_protable, show_custom_errors
from .decorators import is_complete_information_doctor
from .models import Doctor, IdentificationDocument, ApproachUsedTreatment
from .forms import DoctorForm, IdentificationDocumentForm, NickNameForm
from django.contrib import messages

from doctors.utility import check_information_doctor, check_owner_info


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class DetailDoctor(View):
    def get(self, request, doctor_id, *args, **kwargs):
        try:
            # TODO: handle Error DoseNotExsists
            doctor = Doctor.objects.get(id=doctor_id)
            identification_document_list = IdentificationDocument.objects.filter(doctor_id=doctor_id)
            approach_used_treatment = ApproachUsedTreatment.objects.all()
            is_owner_info = check_owner_info(request.user)
            context = {
                "doctor": doctor,
                "identification_document_list": identification_document_list,
                "is_owner_info": is_owner_info,
                "approach_used_treatment": approach_used_treatment,
            }
            return render(request, 'doctors/doctor_detail.html', context)
        except Doctor.DoesNotExist:
            return redirect('page_404')


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class IsVerifyDoctorByStaff(View):
    def get(self, request, *args, **kwargs):
        doctor_id = request.GET['doctor_id']
        doctor = Doctor.objects.get(id=doctor_id)
        if doctor.is_verify == True:
            doctor.is_verify = False
            doctor.save()

            content = "مجوز شما توسط ادمین لغو شد"
            send_notification_in_protable(receiver=doctor.user, content=content, sender=request.user)

            response = {
                'is_taken': True,
                'doctor_id': doctor.id,
                'is_verify': doctor.is_verify
            }
            return JsonResponse(response)
        else:
            doctor.is_verify = True
            doctor.save()

            content = "مجوز شما توسط ادمین تایید شد"
            send_notification_in_protable(receiver=doctor.user, content=content, sender=request.user)

            response = {
                'is_taken': True,
                'doctor_id': doctor.id,
                'is_verify': doctor.is_verify
            }
            return JsonResponse(response)


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class CompletionInformationDoctor(View):
    template_name = 'doctors/completion_information_doctor.html'

    def get(self, request, *args, **kwargs):
        if check_information_doctor(request.user):
            return redirect('/')

        doctor_form = DoctorForm()
        approach_used_treatment = ApproachUsedTreatment.objects.all()
        context = {
            "doctor_form": doctor_form,
            "approach_used_treatment": approach_used_treatment,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        doctor_form = DoctorForm(request.POST, request.FILES)

        if doctor_form.is_valid():
            doctor_new = doctor_form.save(commit=False)
            doctor_new.user = request.user
            doctor_new.save()
            messages.info(request, "اطلاعات به درستی ثبت شد . لطفا مدارک مربوطه را ارسال کنید")
            return redirect('doctors:get_identification_document_doctor')
        else:
            error_message = show_custom_errors(doctor_form.errors)
            messages.error(request, error_message)
            return redirect(request.META.get("HTTP_REFERER"))


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class UpdateInformationDoctor(View):
    def post(self, request):
        doctor_form = DoctorForm(request.POST, request.FILES, instance=request.user.doctor)
        if doctor_form.is_valid():
            doctor_form.save()
            messages.success(request, "اطلاعات ویرایش شد")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            error_message = show_custom_errors(doctor_form.errors)
            messages.error(request, error_message)
            return redirect(request.META.get("HTTP_REFERER"))


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class GetIdentificationDocumentDoctor(View):
    template_name = 'doctors/get_identification_document_doctor.html'

    @method_decorator(is_complete_information_doctor)
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor
        identification_document_list = IdentificationDocument.objects.filter(doctor=doctor)
        identification_document_form = IdentificationDocumentForm()
        context = {
            "identification_document_form": identification_document_form,
            "identification_document_list": identification_document_list,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        identification_document_form = IdentificationDocumentForm(request.POST, request.FILES)
        if identification_document_form.is_valid():
            document_new = identification_document_form.save(commit=False)
            document_new.doctor = request.user.doctor
            document_new.save()
            messages.info(request, "فایل آپلود شد")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            error_message = show_custom_errors(identification_document_form.errors)
            messages.error(request, error_message)
            return redirect(request.META.get("HTTP_REFERER"))


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class DeleteIdentificationDocument(View):
    def get(self, request, pk):
        document = IdentificationDocument.objects.get(pk=pk, doctor=request.user.doctor)
        document.delete()
        messages.success(request, "مدرک شناسایی شما با موفقیت حذف شد")
        return redirect('doctors:get_identification_document_doctor')


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class ListCustomerEachDoctor(View):
    def get(self, request):
        customers = Customer.objects.filter(treating_doctor=request.user.doctor).defer("treating_doctor")
        context = {
            'customers': customers,
        }
        return render(request, 'doctors/list_customers_requested_each_doctor.html', context)

    def post(self, request):
        nick_name_form = NickNameForm(request.POST)
        if nick_name_form.is_valid():
            customer_id = nick_name_form.cleaned_data['customer_id']
            nick_name = nick_name_form.cleaned_data['nick_name']
            customer = Customer.objects.get(id=int(customer_id))
            customer.nick_name = nick_name
            customer.save()
            messages.info(request, "نام مستعار ویرایش شد")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            error_message = show_custom_errors(nick_name_form.errors)
            messages.error(request, error_message)
            return redirect(request.META.get("HTTP_REFERER"))
