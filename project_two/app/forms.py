from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from django.core import validators
from app.models import User


def set_years(start):
    years = []
    st = start
    currentYear = int(datetime.now().year)
    while st <= currentYear:
        years.append(st)
        st += 1
    return years


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
