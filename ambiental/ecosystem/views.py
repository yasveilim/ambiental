from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home.html'


class Login(TemplateView):
    template_name = 'login.html'


class Index(TemplateView):
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
        

class ForgotPassword(TemplateView):
    template_name = 'forgotpassword.html'