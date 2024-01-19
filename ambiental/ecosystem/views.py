from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import CreateUserForm
from django.contrib.auth.models import User


class Home(generic.TemplateView):
    template_name = 'home.html'


class Login(generic.TemplateView):
    template_name = 'login.html'

# class Signup(generic.TemplateView):
#     template_name = 'signup.html'


class Signup(generic.CreateView):  # ecosystem:
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    model = User
    form_class = CreateUserForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(self.object.password)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        # NOTA: toasts
        # https://blog.benoitblanchon.fr/django-htmx-toasts/
        # print('I am here, in invalid', form.errors)
        return super().form_invalid(form)


class Index(generic.TemplateView):
    template_name = 'index/generic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = self.kwargs.get('site')
        context['category'] = site

        match site:
            case "water":
                context['imgmaterial'] = 'agua.jpg'
            case "air-noise":
                context['imgmaterial'] = 'aire.jpg'
            case "waste":
                context['imgmaterial'] = 'residuos.jpg'
            case "recnat-risks":
                context['imgmaterial'] = 'riesgos.jpg'
        return context

    def get_template_names(self):
        slug = self.kwargs.get('site')

        if slug == 'advance':
            return ['index/advance.html']

        elif slug == 'others':
            return ['index/others.html']

        else:
            return ['index/generic.html']


class ForgotPassword(generic.TemplateView):
    template_name = 'forgotpassword.html'
