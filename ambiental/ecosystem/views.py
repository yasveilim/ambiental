# import typing as t
from typing import Any
from sharepoint.sicma import main as sicma_main
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect  # HttpRequest, HttpResponse,
# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from . import forms
from django.contrib.auth.models import User
from . import models

SICMA_AZURE_DB = sicma_main()

class Home(generic.TemplateView):
    template_name = 'home.html'


class Login(generic.TemplateView):
    template_name = 'login.html'


class Nuevo(generic.TemplateView):
    template_name = 'nuevo.html'


class Signup(generic.CreateView):  # ecosystem:
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    model = User
    form_class = forms.CreateUserForm

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
        # print(SICMA_AZURE_DB)

        # ['AIRE Y RUIDO', 'AGUA', 'RESIDUOS', 'RECNAT Y RIESGO', 'OTROS']
        match site:
            case "water":
                context['book'] = SICMA_AZURE_DB['AGUA']
                context['imgmaterial'] = 'agua.jpg'
            case "air-noise":
                context['book'] = SICMA_AZURE_DB['AIRE Y RUIDO']
                context['imgmaterial'] = 'aire.jpg'
            case "waste":
                context['book'] = SICMA_AZURE_DB['RESIDUOS']
                context['imgmaterial'] = 'residuos.jpg'
            case "recnat-risks":
                context['book'] = SICMA_AZURE_DB['RECNAT Y RIESGO']
                context['imgmaterial'] = 'riesgos.jpg'
            case "others":
                context['book'] = SICMA_AZURE_DB['OTROS']
                context['imgmaterial'] = 'others.jpg'

        return context

    def get_template_names(self):
        slug = self.kwargs.get('site')

        if slug == 'advance':
            return ['index/advance.html']
        else:
            return ['index/generic.html']


class ForgotPassword(generic.CreateView):
    #success_url = reverse_lazy('forgotresetcode')  # reverse_lazy('forgotpassword')
    template_name = 'forgotpassword.html'
    model = User# models.RestorePasswordRequest
    form_class = forms.RestorePasswordForm

    # def get_success_url(self):
    #     #reverse_lazy('forgotresetcode', kwargs={'pk': self.object.email})
    #     print("it is url: ", self.success_url.format(pk=self.object.id))
    #     mysuper = super().get_success_url()
    #     print('the super is: ', mysuper)
    #     return mysuper
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        success_url = reverse_lazy('forgotresetcode', kwargs={'pk': self.object.id})

        #if success_url:
        #    url = success_url.format(**self.object.__dict__)
        print('the success url is: ', str(success_url))
        return success_url

    def form_valid(self, form):
        form_obj = form.save(commit=False)


        self.object = User.objects.get(email=form_obj.email)
        print('the email is: ', self.object.email)
        # self.object.set_password(self.object.password)
        # self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print('I am here, in invalid', [form.errors])
        # NOTA: toasts
        # https://blog.benoitblanchon.fr/django-htmx-toasts/
        # print('I am here, in invalid', form.errors)
        return super().form_invalid(form)


class ForgotPasswordUpdate(generic.UpdateView):
    template_name = 'forgotresetcode.html'
    model = models.RestorePasswordRequest
    form_class = forms.ResetcodePasswordForm

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        print('I am here, in get', kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        print('I am here, in post', form, [form.errors])
        return super().post(request, *args, **kwargs)
