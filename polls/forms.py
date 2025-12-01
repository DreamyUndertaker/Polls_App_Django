from django import forms
from .models import QuestionFile


class QuestionFileForm(forms.ModelForm):
    class Meta:
        model = QuestionFile
        fields = ['title', 'file']  # или только 'file', если title не нужен
