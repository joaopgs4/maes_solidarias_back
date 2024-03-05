from django.contrib.auth.models import User
from django.db import models

# Create your models here.

#Para podermos complementar o user do django sem precisar utilizar um abstract user e precisar refazer algumas mecanicas como proteção de senha, utilizamos um Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Genders = (
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
        ('Prefiro não informar', 'Prefiro não informar'),
        ('Outro', 'Outro'),
    )
    User_types = (
        ('Usuario', 'Usuario'),
        ('Administrador', 'Administrador'),
    )
    #Configuração do tipo de usuario. No começo por praticidade
    user_type = models.CharField(max_length=100, choices=User_types, default='Usuario', verbose_name='Tipo Usuario')

    #Reescrita dos valores originais do django user, para facilitar visualização e interação do objeto
    first_name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Nome')
    last_name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Sobrenome')
    email = models.EmailField(max_length=254, null=True, blank=True, verbose_name='E-mail') 

    #outros campos
    images = models.TextField(blank=True, null=True)
    birth = models.DateField(null=True, blank=True, verbose_name='Data de nascimento')
    phone_number = models.CharField(max_length=19, null=True, blank=True, verbose_name='Número de Telefone')
    gender = models.CharField(max_length=20, choices=Genders, null=True, blank=True, verbose_name='Gênero')

    #Campos de acesso
    date_joined = models.DateTimeField(auto_now_add=True)
    last_acces = models.DateTimeField(auto_now=True)