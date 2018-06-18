from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, \
    LogoutView, PasswordResetView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import generic

from .utils import send_confirmation_email
from .forms import LogInForm, SignUpForm, \
    RequestResetPasswordForm, ResetPasswordForm
from .tokens import account_activation_token as aat, \
    password_reset_token as prt


class LogInView(LoginView):
    template_name = 'users/login.html'
    authentication_form = LogInForm

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('komitets:main'))
        else:
            return super().get(request)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(user=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class LogOutView(LogoutView):
    next_page = reverse_lazy('users:login')


class SignUpView(generic.CreateView):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('users:login')

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('komitets:main'))
        else:
            return super().get(request)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_confirmation_email(self.request, user, form.cleaned_data['email'])
        return render(
            self.request, 'users/account_info.html',
            context={'message': 'Please confirm your email address'
                                ' to complete the registration.'}
        )


class ActivateUserView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None \
                and aat.check_token(user, kwargs['token']):
            user.is_active = True
            user.save()
            return render(
                self.request, 'users/account_info.html',
                context={'message': 'Thank you for your email confirmation.'
                                    ' Now you can login your account.'}
            )
        else:
            return render(self.request, 'users/account_info.html',
                          context={'message': 'Activation link is invalid!'})


class ResetPasswordRequestView(PasswordResetView):
    form_class = RequestResetPasswordForm
    template_name = 'users/reset_password_request.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(
                self.request, 'users/account_info.html',
                context={'message': 'Please check your '
                                    'email to reset password.'}
            )
        send_confirmation_email(self.request, user, email, reset_password=True)
        return render(self.request, 'users/account_info.html',
                      context={'message': 'Please check your email'
                                          ' to reset password.'})


class ResetPasswordView(generic.FormView):
    template_name = 'users/password_reset.html'

    def get_form(self, form_class=None):
        return ResetPasswordForm(self.request.user)

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None or not prt.check_token(user, kwargs['token']):
            return render(
                self.request, 'users/account_info.html',
                context={'message': 'Password reset link is invalid!'}
            )
        else:
            return render(self.request, 'users/password_reset.html',
                          context={'form': ResetPasswordForm(user)})

    def form_valid(self, form):
        print(self.request.POST)

    # def post(self, request, *args, **kwargs):
    #     print(dir(request))
    #     form = ResetPasswordForm(user=request.user,
    # password1=kwargs['password1'],
    #  password2=kwargs['password2'])
    #     print(form)
    #     try:
    #         uid = urlsafe_base64_decode(kwargs['uidb64'])
    #         user = User.objects.get(pk=uid)
    #     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    #         user = None
    #     if user is not None and prt.check_token(user, kwargs['token']):
    #
    #         if form.is_valid():
    #             user.set_password('1')
    #             user.save()
    #             return self.form_valid(form)
    #         else:
    #             print(form.error_messages)
    #             return render(self.request, 'users/account_info.html',
    #                           context={'message': 'The two password
    #  fields didn\'t match.'})
    #     else:
    #         return render(self.request, 'users/account_info.html',
    #                       context={'message': 'Password reset
    #  link is invalid!'})
    #
    # def form_valid(self, form):
    #     print('valid')
    #     return super().form_valid(form)
    #
    # def form_invalid(self, form):
    #     print('invalid')
    #     return super().form_invalid(form)
