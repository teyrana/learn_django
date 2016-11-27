from django import forms
from django.forms import ModelForm
from .models import Recipient, City

class RegisterForm( ModelForm ):
    class Meta:
        model= Recipient
        fields = ['email','location']
        field_classes = {
            'email': forms.EmailField,
        }
