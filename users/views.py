from django.shortcuts import render
from django.views import generic


class LoginView(generic.TemplateView):
    template_name = 'users/login.html'

