from django import forms
from django.contrib.auth import get_user_model
from core.models import *

ALL_USERS = get_user_model().objects.all()

class QuestionForm(forms.ModelForm):
    user = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=ALL_USERS, disabled=True)
    text = forms.CharField(widget=forms.Textarea)
    text.widget.attrs.update({'rows': '2'})

    class Meta:
        model = Question
        fields = ['title', 'text', 'user']

class AnswerForm(forms.ModelForm):
    user = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=ALL_USERS, disabled=True)
    question = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Question.objects.all(), disabled=True)
    text = forms.CharField(widget=forms.Textarea)
    text.widget.attrs.update({'rows': '2'})

    class Meta:
        model = Answer
        fields = ['text', 'user', 'question']

class AnswerAcceptanceForm(forms.ModelForm):
    is_accepted = forms.BooleanField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Answer
        fields = ['is_accepted']
