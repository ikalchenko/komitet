from django import forms
from django.contrib.auth import forms as auth_form, password_validation
from django.contrib.auth.models import User


class LogInForm(auth_form.AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', })
    )


class SignUpForm(auth_form.UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', })
    )
    username = auth_form.UsernameField(
        widget=forms.TextInput(attrs={'class': 'form-control', })
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control', })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', })
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects \
            .filter(email=email) \
            .exclude(username=username) \
            .exists():
            raise forms.ValidationError('Email address must be unique.')
        return email


class RequestResetPasswordForm(auth_form.PasswordResetForm):
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control', })
    )


class ResetPasswordForm(auth_form.SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
        strip=False,
    )
    new_password2 = forms.CharField(
        label='New password confirmation',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),

    )


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', })
    )
    username = auth_form.UsernameField(
        widget=forms.TextInput(attrs={'class': 'form-control', })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
