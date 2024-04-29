"""
URL configuration for ambiental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from ecosystem import views

# endpoints
urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("prueba/", views.Prueba.as_view(), name="prueba"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("signup/", views.Signup.as_view(), name="signup"),
    path("index/<slug:site>", views.Index.as_view(), name="index"),
    path("index/", views.Index.as_view(), name="index_no_site"),
    path("forgot-password/", views.ForgotPassword.as_view(), name="forgotpassword"),
    path(
        "forgot-password/<int:pk>/",
        views.ForgotPasswordUpdate.as_view(),
        name="forgotresetcode",
    ),
    path(
        "forgot-password/<int:pk>/<slug:pwd>/",
        views.ForgotPasswordUpdate.as_view(),
        name="forgotresetcode_pwd",
    ),
    # Data request
    path(
        "api/save-material-book/",
        views.SaveMaterialBook.as_view(),
        name="save_material_book",
    ),
    path("api/category/", views.Category.as_view(), name="category"),
    path("api/material/<slug:category>", views.Material.as_view(), name="material"),
    path(
        "api/materialbook/<slug:category>/<int:material>",
        views.MaterialBook.as_view(),
        name="materialbook",
    ),
]
