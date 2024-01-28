# import typing as t
from typing import Any

from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect  # HttpRequest, HttpResponse,
from django.shortcuts import get_object_or_404
# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import BaseUpdateView
from sharepoint.mailbox import send_email
from sharepoint.sicma import SicmaDB

from . import models, utils, forms

SICMA_AZURE_DB = SicmaDB()


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
        # print(SICMA_AZURE_DB.data)

        # ['AIRE Y RUIDO', 'AGUA', 'RESIDUOS', 'RECNAT Y RIESGO', 'OTROS']
        match site:
            case "water":
                context['book'] = SICMA_AZURE_DB.data['AGUA']
                context['imgmaterial'] = 'agua.jpg'
            case "air-noise":
                context['book'] = SICMA_AZURE_DB.data['AIRE Y RUIDO']
                context['imgmaterial'] = 'aire.jpg'
            case "waste":
                context['book'] = SICMA_AZURE_DB.data['RESIDUOS']
                context['imgmaterial'] = 'residuos.jpg'
            case "recnat-risks":
                context['book'] = SICMA_AZURE_DB.data['RECNAT Y RIESGO']
                context['imgmaterial'] = 'riesgos.jpg'
            case "others":
                context['book'] = SICMA_AZURE_DB.data['OTROS']
                context['imgmaterial'] = 'others.jpg'

        return context

    def get_template_names(self):
        slug = self.kwargs.get('site')

        if slug == 'advance':
            return ['index/advance.html']
        else:
            return ['index/generic.html']


class ForgotPassword(generic.CreateView):
    template_name = 'forgotpassword/index.html'
    model = User  # models.RestorePasswordRequest
    form_class = forms.RestorePasswordForm

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""

        success_url = reverse_lazy('forgotresetcode', kwargs={'pk': self.object.id})
        return success_url

    def form_valid(self, form):
        form_obj = form.save(commit=False)
        self.object = get_object_or_404(User, email=form_obj.email)
        form_obj.reset_code = utils.generate_reset_code()
        print("form_obj is: ", type(form_obj), " - ", form_obj.id)
        print('the email is: ', self.object.email, " - ", form_obj.reset_code)
        form_obj.save()
        send_email(SICMA_AZURE_DB.account,
                   self.object.email,
                   'Código de recuperación de contraseña',
                   str(form_obj.reset_code))

        # send_email(account: Account, to: str, subject: str, body: str):
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
    template_name = 'forgotpassword/resetcode.html'
    model = models.RestorePasswordRequest
    form_class = forms.ResetcodePasswordForm

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = get_object_or_404(User, id=kwargs['pk'])
        return super(BaseUpdateView, self).get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        print('I am here, in post', form, [form.errors])
        return super().post(request, *args, **kwargs)
