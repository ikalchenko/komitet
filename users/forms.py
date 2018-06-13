from django import forms
from django.contrib.auth import forms as auth_form


class LogInForm(auth_form.AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }))


class SignUpForm(auth_form.UserCreationForm):
    username = auth_form.UsernameField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }))
