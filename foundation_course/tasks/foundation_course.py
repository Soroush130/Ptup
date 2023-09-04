from django.contrib import messages

from customers.models import Customer
from foundation_course.models import QuestionnaireAnswer, Questionnaire


def check_foundation_course(request, customer_id: int):
    customer = Customer.objects.get(id=customer_id)
    questionnaire_list = Questionnaire.objects.all()
    questionnaire_answer_list = QuestionnaireAnswer.objects.filter(customer=customer)

    if questionnaire_list.count() == questionnaire_answer_list.count():
        disease_information = customer.customer_disease_information.filter(is_finished=False).first()
        disease_information.is_foundation_course = True
        disease_information.save()
        messages.success(request, "شما تمامی پرسشنامه ها را تکمیل کردید")

    else:
        pass
