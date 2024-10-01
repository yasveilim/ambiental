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
from datetime import datetime


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

        if not self.request.user.is_authenticated:

            user = authenticate(
                self.request,
                username=user_base.username,
                password=form["password"].value(),
            )

            if user is not None:
                login(self.request, user)

            else:
                return JsonResponse({"message": "Invalid user or password"}, status=404)

        return JsonResponse({"message": "Ok"})

    def form_invalid(self, form):
        print("Form invalid")
        return super().form_invalid(form)


class Signup(generic.CreateView):
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
        is_staff = self.request.user.is_staff
        usersList = None

        context["category"] = site
        context["currentUser"] = {
            "name": self.request.user.username,
            "isStaff": is_staff,
        }

        if is_staff:
            usersList = User.objects.filter(is_staff=False).values("username", "id")
            context["usersList"] = usersList

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
        user = self.request.user
        if not user.is_authenticated:
            return redirect("/")

        if user.is_staff:
            user = User.objects.filter(is_staff=False).first()

        user_sharepoint_dir = models.UserSharepointDir.objects.filter(user=user).first()

        if user_sharepoint_dir is None:
            unique_user_dir_name = SICMA_AZURE_DB.generate_unique_user_dir()
            user_sharepoint_dir = models.UserSharepointDir.objects.create(
                user=user, name=unique_user_dir_name
            )

        SICMA_AZURE_DB.load_data(user_sharepoint_dir.name)

        return super().dispatch(request, *args, **kwargs)


class AdminUsers(Index):
    template_name = "index/adminusers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_staff = self.request.user.is_staff
        usersList = None

        # context["category"] = "admin_user"
        context["currentUser"] = {
            "name": self.request.user.username,
            "isStaff": is_staff,
        }

        context["sheet"] = "admin-users"
        context["fakerange"] = range(1, 110)

        if is_staff:
            usersList = User.objects.filter(is_staff=False).values(
                "username", "last_name",  "email", "id"
            )
            context["usersList"] = usersList

        return context

    def get_template_names(self):
        return ["index/adminusers.html"]

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/")

        return super(generic.TemplateView, self).dispatch(request, *args, **kwargs)

        
class AdminUsersAPI(generic.View):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode("utf-8")
        body_data = json.loads(body_unicode)

        user = User.objects.create(
            username=body_data["username"],
            last_name=body_data["lastname"],
            #password=body_data["password"],
            email=body_data["email"],
            is_staff=False,
        )

        user.set_password(body_data["password"])
        user.save()

        return JsonResponse({"ok": 200})

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")

        if user_id is None:
            users = User.objects.filter(is_staff=False).values("username", "last_name", "email", "id")
            return JsonResponse({"users": list(users)})

        user = User.objects.get(id=user_id)

        return JsonResponse({"username": user.username, "lastname": user.last_name, "email": user.email})

    def put(self, request, *args, **kwargs):

        user_id = kwargs["pk"]


        body_unicode = request.body.decode("utf-8")
        body_data = json.loads(body_unicode)


        user = User.objects.get(id=user_id)
        user.username = body_data["username"]
        user.last_name = body_data["lastname"]
        user.email = body_data["email"]
        
        user.save()


        return JsonResponse({"ok": 200})
    
    def delete(self, request, *args, **kwargs):
        print("Deleting user: ", kwargs)
        user_id = kwargs["pk"]

        user = User.objects.get(id=user_id)
        user.delete()

        print("User deleted: ", user, user_id)

        return JsonResponse({"ok": 200})
    
    def dispatch(self, request, *args, **kwargs):
        print("Dispatching user: ", kwargs)
        if not self.request.user.is_authenticated:
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)


class ForgotPassword(generic.CreateView):
    template_name = "forgotpassword/index.html"
    model = User
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



class SaveCommentMaterialBook(generic.View):

    def post(self, request, *args: str, **kwargs: Any) -> HttpResponse:
        user = self.request.user

        body_unicode = request.body.decode("utf-8")
        body_data = json.loads(body_unicode)

        if user.is_staff:

            user = User.objects.get(id=body_data["targetUser"]["id"])

        book_id = body_data["bookId"]
        category = body_data["category"]

        tag = category.replace("-", "_")
        sharepoint_path = models.AmbientalBookSharepointPath.objects.filter(
            category=tag,
            user=user,
            book_id=book_id,
        ).first()

        comment = None
        if sharepoint_path:
            comment = models.BookSharepointComment.objects.filter(
                book=sharepoint_path
            ).first()

            if comment is None:
                comment = models.BookSharepointComment.objects.create(
                    book=sharepoint_path,
                    comment="",
                )

        else:
            error_message = '{"error": "NotFound"}'
            return HttpResponse(
                error_message, content_type="application/json", status=404
            )

        return JsonResponse({"ok": 200, "comment": comment.comment})

    def put(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user = self.request.user

        body_unicode = request.body.decode("utf-8")
        body_data = json.loads(body_unicode)

        if user.is_staff:
            user = User.objects.get(id=body_data["targetUser"]["id"])

        else:
            return JsonResponse({"error": "Forbidden"}, status=403)

        book_id = body_data["bookId"]
        category = body_data["category"]
        comment_text = body_data["comment"]

        tag = category.replace("-", "_")
        sharepoint_path = models.AmbientalBookSharepointPath.objects.filter(
            category=tag,
            user=user,
            book_id=book_id,
        ).first()

        if sharepoint_path is None:
            error_message = '{"error": "NotFound"}'
            return HttpResponse(
                error_message, content_type="application/json", status=404
            )

        comment = models.BookSharepointComment.objects.filter(
            book=sharepoint_path
        ).first()

        if comment:
            comment.comment = comment_text
            comment.save()

        else:
            error_message = '{"error": "NotFound"}'
            return HttpResponse(
                error_message, content_type="application/json", status=404
            )

        return JsonResponse({"ok": 200, "comment": comment.comment})

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)


class SaveMaterialBook(generic.View):

    # Dada este metodo dejango como obtendria los valores que alguien me envia en un form

    def post(self, request, *args: str, **kwargs: Any) -> HttpResponse:

        print(self.request.user, request.user)

        user = self.request.user
        if user.is_staff:
            target_user = json.loads(request.POST.get("targetUser"))
            user = User.objects.get(id=target_user["id"])

        # help(models.UserSharepointDir.objects.first)
        user_sharepoint_dir = models.UserSharepointDir.objects.filter(user=user).first()

        if user_sharepoint_dir is None:
            unique_user_dir_name = SICMA_AZURE_DB.generate_unique_user_dir()
            user_sharepoint_dir = models.UserSharepointDir.objects.create(
                user=user, name=unique_user_dir_name
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
            user=user,
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

        user = self.request.user
        if user.is_staff:
            target_user = json.loads(request.POST.get("targetUser"))
            user = User.objects.get(id=target_user["id"])

        user_sharepoint_dir = models.UserSharepointDir.objects.filter(user=user).first()

        SICMA_AZURE_DB.load_data(user_sharepoint_dir.name)

        return super().dispatch(request, *args, **kwargs)


def get_user_sharepoint_dir(user: User) -> models.UserSharepointDir:
    user_sharepoint_dir = models.UserSharepointDir.objects.filter(user=user).first()

    if user_sharepoint_dir is None:
        unique_user_dir_name = SICMA_AZURE_DB.generate_unique_user_dir()
        user_sharepoint_dir = models.UserSharepointDir.objects.create(
            user=user, name=unique_user_dir_name
        )

    return user_sharepoint_dir


class Material(generic.View):

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        category = self.kwargs.get("category")

        materal = get_materal_from_category(category) or {}

        return JsonResponse({"names": [x for x in materal.keys()]})

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect("/")

        if user.is_staff:
            body_unicode = request.body.decode("utf-8")
            body_data = json.loads(body_unicode)
            user = User.objects.get(id=body_data["targetUser"]["id"])

        user_sharepoint_dir = get_user_sharepoint_dir(user)

        SICMA_AZURE_DB.load_data(user_sharepoint_dir.name)
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

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        materials = get_materal_from_category(kwargs["category"]) or {}

        materials_namesidx = {k: v for k, v in enumerate(materials.keys())}
        name = materials_namesidx.get(kwargs["material"]) or ""
        material = materials.get(name) or []

        user = self.request.user
        if user.is_staff:
            body_unicode = request.body.decode("utf-8")
            body_data = json.loads(body_unicode)
            user = User.objects.get(id=body_data["targetUser"]["id"])

        for mat in material:
            mat["name"] = str(mat["doc_number"]) + " " + mat["name"]
            mat["deliveryDate"] = "No recibido"
            category = kwargs["category"]
            tag = category.replace("-", "_")
            sharepoint_path = models.AmbientalBookSharepointPath.objects.filter(
                category=tag,
                user=user,
                book_id=mat["doc_number"],
            ).first()

            if sharepoint_path:
                mat["advance"] = "DELIVERED"
                mat["deliveryDate"] = sharepoint_path.receipt_date
                # sharepoint_path.receipt_date
            elif mat["advance"] == "DELIVERED":
                mat["advance"] = "PENDING"

        #
        # print(material)

        return JsonResponse({"items": material})

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect("/")

        if user.is_staff:
            body_unicode = request.body.decode("utf-8")
            body_data = json.loads(body_unicode)
            user = User.objects.get(id=body_data["targetUser"]["id"])

        user_sharepoint_dir = models.UserSharepointDir.objects.filter(user=user).first()

        SICMA_AZURE_DB.load_data(user_sharepoint_dir.name)
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
