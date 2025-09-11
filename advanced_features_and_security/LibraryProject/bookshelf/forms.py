from django import forms
from .models import Book  # assuming you already have a Book model

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']  # adjust fields as needed
