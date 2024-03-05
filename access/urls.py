from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('<int:id>/', views.user_edit),
    path('', views.users),

]