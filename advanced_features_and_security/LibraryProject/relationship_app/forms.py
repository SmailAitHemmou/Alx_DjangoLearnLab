from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # Use a ForeignKey to Author, not a CharField
        fields = ['title', 'author', 'published_date']