from django import forms


class PracticeAnswerForm(forms.Form):
    healing_day = forms.IntegerField()
    content = forms.CharField(widget=forms.Textarea, required=False)
    file = forms.FileField(widget=forms.FileInput, required=False)

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        file = cleaned_data.get('file')

        if not content and not file:
            raise forms.ValidationError("فیلد توضیحات یا فایل وارد نشده است")

        return cleaned_data


class DayFeedbackForm(forms.Form):
    practice_answer_id = forms.IntegerField()
    subject = forms.CharField()
    content = forms.CharField(widget=forms.TextInput)