from django import forms
from .models import Book
from .forms import ExampleForm


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]

class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=100, strip=True)

class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
