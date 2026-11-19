from django import forms
from django.utils import timezone

from .models import Book, Author


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['created_by']
        widgets = {
            'genres': forms.CheckboxSelectMultiple,
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if title.isdigit():
            raise forms.ValidationError('Название не может состоять только из цифр.')
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) > 2000:
            raise forms.ValidationError('Описание не должно быть длиннее 2000 символов.')
        return description

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio']
