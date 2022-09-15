from dataclasses import field
from re import A
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

from .models import Account, Profile


from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=63, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=63, widget=forms.PasswordInput)
    class Meta:
        model = Account
        fields = ("username", "email", "password1", "password2")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ("username", "email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

# class LoginForm(forms.ModelForm):
#     # username_or_email = forms.CharField(max_length=50)
#     # password = forms.CharField(max_length=20, widget=forms.PasswordInput())

#     class Meta:
#         model = Account
#         fields = ("username", "password")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


