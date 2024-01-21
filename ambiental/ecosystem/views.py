import typing as t
from sharepoint.sicma import main as sicma_main
from django.http import HttpResponseRedirect  # HttpRequest, HttpResponse,
# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import CreateUserForm
from django.contrib.auth.models import User

SICMA_AZURE_DB = sicma_main()

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
        print(SICMA_AZURE_DB)

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


class ForgotPassword(generic.TemplateView):
    template_name = 'forgotpassword.html'
