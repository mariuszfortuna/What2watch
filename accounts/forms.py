from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserUpdateView(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'groups']
        widgets = {
            #'user_permissions': forms.CheckboxSelectMultiple(),
            'groups': forms.CheckboxSelectMultiple()
        }
