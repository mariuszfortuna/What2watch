from django import forms

from .models import Person


class AddPersonModelForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    photo = forms.ImageField()

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'photo']

    photo = forms.ImageField(required=False)
