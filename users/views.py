from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.models import User

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

    # def form_valid(self, form):
    #     username = form.cleaned_data['username']
    #     password1 = form.cleaned_data['password1']
    #     password2 = form.cleaned_data['password2']
    #     user = User.objects.create(username=username)
    #     if password1 == password2:
    #         user.set_password(password1)
    #         user.save()
    #     return super().form_valid(form)




