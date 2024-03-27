from django import forms
from .models import QuestionFile


class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionFile
        fields = ['title', 'file']
        required = ['title', 'file']
