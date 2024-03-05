from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_usuario/', views.cadastra_user),
]