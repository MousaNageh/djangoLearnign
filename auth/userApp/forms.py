from django import forms
from django.contrib.auth.models import User
from userApp.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")


class UserProfile(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ("profile_site", "profile_pic")


class UserLogin(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(), max_length=100, required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(), max_length=100, required=True)
