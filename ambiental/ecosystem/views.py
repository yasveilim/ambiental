from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home.html'


class Login(TemplateView):
    template_name = 'login.html'


class Index(TemplateView):
    template_name = 'index.html'


class ForgotPassword(TemplateView):
    template_name = 'forgotpassword.html'