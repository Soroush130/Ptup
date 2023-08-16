from rest_framework import serializers
from django.db import transaction
from foundation_course.models import Questionnaire, Question, QuestionOption


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = (
            'id',
            'title',
            'description',
            'number_of_options',
            'type',
            'dependency',
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'questionnaire',
            'row',
            'text'
        )


class QuestionWriteSerializer(serializers.Serializer):
    questionnaire_id = serializers.IntegerField()
    row = serializers.IntegerField()
    text = serializers.CharField()
    question_option_list = serializers.ListField(child=serializers.DictField())

    def create(self, validated_data):
        questionnaire_id = validated_data.get("questionnaire_id")
        row = validated_data.get("row")
        text = validated_data.get("text")
        question_option_list = validated_data.pop("question_option_list")

        with transaction.atomic():
            question = Question.objects.create(
                questionnaire_id=questionnaire_id,
                row=row,
                text=text
            )

            for question_option in question_option_list:
                question_option_new: QuestionOption = QuestionOption.objects.create(
                    question=question,
                    coefficient=question_option['coefficient'],
                    text=question_option['text'],
                    row=question_option['row'],
                )

            return question
