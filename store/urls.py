from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('categoria/', views.categoria ),
]

urlpatterns = [
    path('item/', admin.site.urls),
]