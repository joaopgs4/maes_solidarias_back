from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('categoria/', views.categoria),
    path('<int:id>', views.items_id),
    path('', views.items),
]
