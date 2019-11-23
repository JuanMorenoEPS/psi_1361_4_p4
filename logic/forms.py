from django import forms
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from datamodel.models import Move


class SignupForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6)
    password2 = forms.CharField(widget=forms.PasswordInput(), min_length=6)

    class Meta:
        model = User
        fields = ('username', 'password')


class LogInForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class MoveForm(forms.ModelForm):
    origin = forms.IntegerField(initial=0, required=True)
    target = forms.IntegerField(initial=0, required=True)


    class Meta:
        model = Move
        fields = ('origin', 'target')








