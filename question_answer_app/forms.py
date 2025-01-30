from django import forms


class QuestionForm(forms.Form):
    question_text = forms.CharField(widget=forms.TextInput)


class AnswerForm(forms.Form):
    answer_text = forms.CharField(widget=forms.TextInput)
