from django import forms
from chatapp.models import Post, AuthUser, Comment
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    user_profile = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "content", "img")
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control editable medium-editor-textarea'}),
            "img": forms.FileInput(attrs={"class": "form-control"})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), required=True)
