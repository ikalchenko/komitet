from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic

from .tokens import account_activation_token
from .forms import LogInForm, SignUpForm


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

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        message = render_to_string('users/account_activation_email.html', {
            'user': user, 'domain': current_site.domain,
            'uid': str(urlsafe_base64_encode(force_bytes(user.pk)), encoding='utf-8'),
            'token': account_activation_token.make_token(user),
        })
        mail_subject = 'Activate your Komitet account.'
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return render(self.request, 'users/account_activation_info.html',
                      context={'message': 'Please confirm your email address to complete the registration.'})


class ActivateUserView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            user = None
        if user is not None and account_activation_token.check_token(user, kwargs['token']):
            user.is_active = True
            user.save()
            login(request, user)
            return render(self.request, 'users/account_activation_info.html',
                          context={'message': 'Thank you for your email confirmation. Now you can login your account.'})
        else:
            return render(self.request, 'users/account_activation_info.html',
                          context={'message': 'Activation link is invalid!'})


class ResetPasswordView(PasswordResetView):
    pass
