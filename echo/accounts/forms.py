from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm, EmailField

from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        exclude = ("first_name", "last_name")


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'vk', 'telegram', 'whatsup', 'facebook', 'twitter', 'instagram']
