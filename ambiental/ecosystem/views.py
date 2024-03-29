# import typing as t
import json
from typing import Any
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
# HttpRequest, HttpResponse,
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import BaseUpdateView

from sharepoint.mailbox import send_email
from sharepoint.sicma import SicmaDB
from . import models, utils, forms
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import JsonResponse



SICMA_AZURE_DB = SicmaDB()


class Home(generic.TemplateView):
    template_name = 'home.html'


class Prueba(generic.TemplateView):
    template_name = 'prueba.html'


class Logout(generic.RedirectView):
    pattern_name = "home"

    def get(self, request, *args, **kwargs):
        logout(request)

        return super().get(request, *args, **kwargs)


# material
class Login(generic.CreateView):
    success_url = reverse_lazy('index', kwargs={'site': 'air-noise'})
    template_name = 'login.html'
    model = User
    form_class = forms.LoginUserForm

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""

        if self.success_url:
            url = self.success_url.format({'site': 'air-noise'})
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model."
                )
        return url

    def form_valid(self, form: forms.LoginUserForm):
        legit_url = self.get_success_url()
        user_base = get_object_or_404(User, email=form['email'].value())
        print("Form valid / ", self.request.user, ' / ', self.request.user.is_authenticated)
        
        if not self.request.user.is_authenticated:
            
            user = authenticate(
                self.request,
                username=user_base.username,
                password=form['password'].value()
            )

            print("My user is: ", user)
            if user is not None:
                login(self.request, user)
            
            else:
                return JsonResponse({'message': 'Invalid user or password'}, status=404)

        return JsonResponse({'message': 'Ok'}) # HttpResponseRedirect(legit_url)

    def form_invalid(self, form):
        print("Form invalid")
        return super().form_invalid(form)


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
        
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/')
        
        return super().dispatch(request, *args, **kwargs)


class ForgotPassword(generic.CreateView):
    template_name = 'forgotpassword/index.html'
    model = User  # models.RestorePasswordRequest
    form_class = forms.RestorePasswordForm

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""

        success_url = reverse_lazy('forgotresetcode', kwargs={
                                   'pk': self.object.id})
        return success_url

    def form_valid(self, form):
        form_obj = form.save(commit=False)
        self.object = get_object_or_404(User, email=form_obj.email)
        form_obj.reset_code = utils.generate_reset_code()
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


class Material(generic.View):

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return JsonResponse({
            "water": "Agua",
            "air-noise": "Aire y ruído",
            "waste": "Residuos",
            "recnat-risks": "RECNAT y riesgo"
        })
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/')
        
        return super().dispatch(request, *args, **kwargs)
    

class MaterialBook(generic.View):

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        # "water" SICMA_AZURE_DB.data['AGUA']
        #print(kwargs['material'], SICMA_AZURE_DB.data['AGUA'])

        # TODO: Optimize this together with the other match.
        material = ""
        match kwargs['material']:
            case "water": material = 'AGUA'
            case "air-noise": material = 'AIRE Y RUIDO'
            case "waste": material = 'RESIDUOS'
            case "recnat-risks": material = 'RECNAT Y RIESGO'

        # super(generic.View, self).get(request, *args, **kwargs)
        message = { "error": [f"The material {material} does not exist"] }
        material_document = SICMA_AZURE_DB.data.get(material) or message
        return JsonResponse(material_document)
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/')
        
        return super().dispatch(request, *args, **kwargs)
    
#from django.http import JsonResponse
#from django.views import View

# class MiVista(View):
#     def get(self, request, *args, **kwargs):
#         datos = {
#             # Tus datos aquí
#         }
#         return JsonResponse(datos)

class ForgotPasswordUpdate(generic.UpdateView):
    template_name = 'forgotpassword/resetcode.html'
    model = models.RestorePasswordRequest
    form_class = forms.ResetcodePasswordForm

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super(BaseUpdateView, self).get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        # Validate reset code
        get_object_or_404(models.RestorePasswordRequest,
                          reset_code=kwargs['pk'])

        return HttpResponse(json.dumps({'status': 'Ok'}), content_type="application/json", status=200)

    def put(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        reset_code_instance = get_object_or_404(
            models.RestorePasswordRequest, reset_code=kwargs['pk'])
        user_owner = get_object_or_404(User, email=reset_code_instance.email)
        user_owner.set_password(kwargs['pwd'])
        user_owner.save()

        return HttpResponse(json.dumps({'status': 'Ok'}), content_type="application/json", status=200)
