# import typing as t
import json
from typing import Any
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User

# HttpRequest, HttpResponse,
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
import os

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
import json


SICMA_AZURE_DB = SicmaDB()


class Home(generic.TemplateView):
    template_name = "home.html"


class Prueba(generic.TemplateView):
    template_name = "prueba.html"


class Logout(generic.RedirectView):
    pattern_name = "home"

    def get(self, request, *args, **kwargs):
        logout(request)

        return super().get(request, *args, **kwargs)


# material
class Login(generic.CreateView):
    success_url = reverse_lazy("index", kwargs={"site": "air-noise"})
    template_name = "login.html"
    model = User
    form_class = forms.LoginUserForm

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""

        if self.success_url:
            url = self.success_url.format({"site": "air-noise"})
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
        user_base = get_object_or_404(User, email=form["email"].value())
        # print("Form valid / ", self.request.user, ' / ', self.request.user.is_authenticated)

        if not self.request.user.is_authenticated:

            user = authenticate(
                self.request,
                username=user_base.username,
                password=form["password"].value(),
            )

            print("My user is: ", user)
            if user is not None:
                login(self.request, user)

            else:
                return JsonResponse({"message": "Invalid user or password"}, status=404)

        # HttpResponseRedirect(legit_url)
        return JsonResponse({"message": "Ok"})

    def form_invalid(self, form):
        print("Form invalid")
        return super().form_invalid(form)


class Signup(generic.CreateView):  # ecosystem:
    success_url = reverse_lazy("login")
    template_name = "signup.html"
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


def pretty_print_dict(d):
    with open("file.json", "w") as file:
        print(json.dumps(d, indent=4, sort_keys=True), file=file)


def get_materal_from_category(category: str):
    match category:
        case "water":
            return SICMA_AZURE_DB.data["AGUA"]
        case "air-noise":
            return SICMA_AZURE_DB.data["AIRE Y RUIDO"]
        case "waste":
            return SICMA_AZURE_DB.data["RESIDUOS"]
        case "recnat-risks":
            return SICMA_AZURE_DB.data["RECNAT Y RIESGO"]
        case "others":
            return SICMA_AZURE_DB.data["OTROS"]


class Index(generic.TemplateView):
    template_name = "index/generic.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = self.kwargs.get("site")
        context["category"] = site
        pretty_print_dict(SICMA_AZURE_DB.data)

        context["book"] = get_materal_from_category(site)

        return context

    def get_template_names(self):
        slug = self.kwargs.get("site")

        if slug == "advance":
            return ["index/advance.html"]
        else:
            return ["index/generic.html"]

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)


class ForgotPassword(generic.CreateView):
    template_name = "forgotpassword/index.html"
    model = User  # models.RestorePasswordRequest
    form_class = forms.RestorePasswordForm

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""

        success_url = reverse_lazy("forgotresetcode", kwargs={"pk": self.object.id})
        return success_url

    def form_valid(self, form):
        form_obj = form.save(commit=False)
        self.object = get_object_or_404(User, email=form_obj.email)
        form_obj.reset_code = utils.generate_reset_code()
        form_obj.save()

        send_email(
            SICMA_AZURE_DB.account,
            self.object.email,
            "Código de recuperación de contraseña",
            str(form_obj.reset_code),
        )

        # send_email(account: Account, to: str, subject: str, body: str):
        # self.object.set_password(self.object.password)
        # self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print("I am here, in invalid", [form.errors])
        # NOTA: toasts
        # https://blog.benoitblanchon.fr/django-htmx-toasts/
        # print('I am here, in invalid', form.errors)
        return super().form_invalid(form)


from time import sleep


# def assign_sharepoint_directory(user_name: str):#    pass


class SaveMaterialBook(generic.View):

    # Dada este metodo dejango como obtendria los valores que alguien me envia en un form

    def post(self, request, *args: str, **kwargs: Any) -> HttpResponse:

        print(self.request.user, request.user)

        # help(models.UserSharepointDir.objects.first)
        user_sharepoint_dir = models.UserSharepointDir.objects.filter(
            user=self.request.user
        ).first()

        if user_sharepoint_dir is None:
            unique_user_dir_name = SICMA_AZURE_DB.generate_unique_user_dir()
            user_sharepoint_dir = models.UserSharepointDir.objects.create(
                user=self.request.user, name=unique_user_dir_name
            )

        # book_id, category, document
        book_id = request.POST.get("book_id")
        category = request.POST.get("category")
        document_name = request.POST.get("document_name")  # or "name"
        document = request.FILES.get("document")

        # Save the file (document) in to a local directory
        # document = request.FILES.get('document')

        fs = FileSystemStorage()
        path = os.path.join(fs.location, "documents", document.name)
        filename = fs._save(path, document)
        uploaded_file_url = fs.url(filename)

        # request.body / request.body.decode()
        # TODO: Esto debería obtener un documento binario y guardarlo en la carpeta del usuario en sharepoint
        # TODO: El nombre del archivo debería ser el mismo que el del documento (obtener el nombre del frontend)
        print(self.kwargs, request, self.args, args)

        # return JsonResponse({"ok": 200})
        tag = category.replace("-", "_")
        new_book = models.AmbientalBookSharepointPath.objects.create(
            user=self.request.user,
            category=tag,
            book_id=book_id,
            # text_path=self.kwargs.get("text_path"),
        )

        # dirname=#f"{user_sharepoint_dir.name}/{bool_id} {document_name}",
        # material=models.AmbientalBookSharepointPath.get_category_tag(tag),
        material_folder = SICMA_AZURE_DB.create_material_folder(
            material=models.AmbientalBookSharepointPath.get_category_tag(tag),
            id_book=book_id,
            dirname=user_sharepoint_dir.name,
            name_book=document_name,
        )

        material_folder.upload_file(path)

        print(material_folder.child_count)

        # store_folder.upload_file()

        # materials = get_materal_from_category(kwargs["category"]) or {}

        # materials_namesidx = {k: v for k, v in enumerate(materials.keys())}
        # name = materials_namesidx.get(kwargs["material"]) or ""
        # material = materials.get(name) or []

        # JsonResponse({"items": material})\
        return JsonResponse({"ok": 200})

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)


class Material(generic.View):

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        category = self.kwargs.get("category")

        materal = get_materal_from_category(category) or {}

        return JsonResponse({"names": [x for x in materal.keys()]})

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)


class Category(generic.View):

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return JsonResponse(
            {
                "water": "Agua",
                "air-noise": "Aire y ruído",
                "waste": "Residuos",
                "recnat-risks": "RECNAT y riesgo",
            }
        )

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)


class MaterialBook(generic.View):

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        materials = get_materal_from_category(kwargs["category"]) or {}

        materials_namesidx = {k: v for k, v in enumerate(materials.keys())}
        name = materials_namesidx.get(kwargs["material"]) or ""
        material = materials.get(name) or []

        print(kwargs["category"], kwargs["material"], name, materials_namesidx)

        return JsonResponse({"items": material})

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)


class ForgotPasswordUpdate(generic.UpdateView):
    template_name = "forgotpassword/resetcode.html"
    model = models.RestorePasswordRequest
    form_class = forms.ResetcodePasswordForm

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super(BaseUpdateView, self).get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        # Validate reset code
        get_object_or_404(models.RestorePasswordRequest, reset_code=kwargs["pk"])

        return HttpResponse(
            json.dumps({"status": "Ok"}), content_type="application/json", status=200
        )

    def put(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        reset_code_instance = get_object_or_404(
            models.RestorePasswordRequest, reset_code=kwargs["pk"]
        )
        user_owner = get_object_or_404(User, email=reset_code_instance.email)
        user_owner.set_password(kwargs["pwd"])
        user_owner.save()

        return HttpResponse(
            json.dumps({"status": "Ok"}), content_type="application/json", status=200
        )
