from django.forms import ModelForm
from django import forms
from .models import Question, Choice


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']


class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']


class VoteForm(forms.Form):
    def __init__(self, *args, **kwargs):  # change how form behaves on init
        self.question = kwargs.pop('question')  # take "question" kwarg
        super().__init__(*args, **kwargs)  # run default init code
        # set choices for a provided question
        self.fields['choice'].queryset = self.question.choice_set.all()
    # start with empty choices - set of choices depends on question provided to the form
    choice = forms.ModelChoiceField(queryset=Choice.objects.none())
