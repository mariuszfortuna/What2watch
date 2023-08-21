from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise ValidationError('passwords are not the same')
        return cleaned_data


class UserUpdateView(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'groups', 'user_permissions']
        widgets = {
            'user_permissions': forms.CheckboxSelectMultiple(),
            'groups': forms.CheckboxSelectMultiple()
        }
