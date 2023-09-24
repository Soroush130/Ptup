from django import forms


class FollowUpQuestionForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.HiddenInput)
    score = forms.IntegerField()

    def clean_score(self):
        score = self.cleaned_data.get('score')

        if 1 <= score <= 10:
            return score
        else:
            raise forms.ValidationError("نمره وارد شده معتبر نیست")
