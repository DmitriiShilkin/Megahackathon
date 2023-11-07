from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Profile


class PositionForm(forms.Form):
    position = forms.CharField()


class DateInput(forms.DateTimeInput):
    input_type = 'date'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'vk', 'telegram', 'whatsup', 'facebook', 'twitter', 'instagram']


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=40)
    email = forms.EmailField(max_length=50)
    topic = forms.CharField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=1000)
