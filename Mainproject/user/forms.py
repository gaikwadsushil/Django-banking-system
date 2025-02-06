from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact_detail = forms.CharField(max_length=13, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'contact_detail', 'password1', 'gender', 'd_o_b',]

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30,label="Email or Username")
    password = forms.CharField(max_length=30,widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'contact_detail', 'gender', 'd_o_b']