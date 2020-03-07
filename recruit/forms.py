from django import forms
from .models import Application
from django.forms import ModelForm
from django.contrib.auth.models import User

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['q1', 'q2', 'q3', 'q4']

class SignupForm(ModelForm):
    password_check = forms.CharField(max_length=200, widget=forms.PasswordInput())
    field_order=['username','password','password_check','last_name','first_name','email']
    class Meta:
        model = User
        widget = {'password':forms.PasswordInput}
        fields = ['username','password','last_name','first_name','email']

class SigninForm(ModelForm):
    class Meta:
        model = User
        widgets = {'password':forms.PasswordInput}
        fields = ['username','password']