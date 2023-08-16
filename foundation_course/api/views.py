from rest_framework import viewsets
from rest_framework.response import Response

from foundation_course.api.serializers import QuestionnaireSerializer, QuestionSerializer, QuestionWriteSerializer
from foundation_course.models import Questionnaire, Question


class QuestionnaireViewSet(viewsets.ViewSet):

    def list(self, request, **kwargs):
        query = Questionnaire.objects.all().order_by('id')
        serializer = QuestionnaireSerializer(query, many=True)
        return Response(serializer.data)

    def create(self, request, **kwargs):
        return Response('serializer.data')


class QuestionViewSet(viewsets.ViewSet):

    def list(self, request, **kwargs):
        query = Question.objects.all().order_by('id')
        serializer = QuestionSerializer(query, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = QuestionWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('ساخته شد')