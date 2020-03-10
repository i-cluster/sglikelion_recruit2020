from django import forms
from .models import Application, Profile
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ['q1', 'q2', 'q3', 'q4', 'q5']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ['password1', 'password2', 'email', 'last_name']
        for field_name in class_update_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'last_name',
        )
        
class SigninForm(ModelForm):
    class Meta:
        model = User
        widgets = {'password':forms.PasswordInput}
        fields = ['username','password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)