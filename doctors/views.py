from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator

from .decorators import is_complete_information_doctor
from .models import Doctor, IdentificationDocument, ApproachUsedTreatment
from .forms import DoctorForm, IdentificationDocumentForm
from django.contrib import messages

from .utility import check_information_doctor


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
        doctor_form = DoctorForm(request.POST)

        if doctor_form.is_valid():
            doctor_new = doctor_form.save(commit=False)
            doctor_new.user = request.user
            doctor_new.save()
            messages.info(request, "اطلاعات به درستی ثبت شد . لطفا مدارک مربوطه را ارسال کنید")
            return redirect('doctors:get_identification_document_doctor')
        else:
            print('>>>>>>>>>>>>>>> ERRORS <<<<<<<<<<<<<<<')
            print(doctor_form.errors)
            print('-' * 60)
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
            print('>>>>>>>>>>>>>>> ERRORS <<<<<<<<<< ')
            print(identification_document_form.errors)
            print('-' * 60)
            return redirect(request.META.get("HTTP_REFERER"))


@method_decorator(login_required(login_url="accounts:login"), name='dispatch')
class DeleteIdentificationDocument(View):
    def get(self, request, pk):
        document = IdentificationDocument.objects.get(pk=pk, doctor=request.user.doctor)
        document.delete()
        messages.success(request, "مدرک شناسایی شما با موفقیت حذف شد")
        return redirect('doctors:get_identification_document_doctor')
