from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


from . import models
import json


#REMOVER ANTES DE POSTAR
@csrf_exempt
def users(request):
    try:
        if request.method == 'GET':
            usuarios = models.Profile.objects.all()
            
            lista_usuarios = [{
                'id': usuario.id,
                'first_name': usuario.first_name,
                'last_name': usuario.last_name,
                'email': usuario.email,
                'birth': usuario.birth,
                'phone_number': usuario.phone_number,
                'gender': usuario.gender,
                'date_joined': usuario.date_joined,
                'last_acces': usuario.last_acces,
                'user_type': usuario.user_type,
                'images': usuario.images
            } for usuario in usuarios]
            
            return JsonResponse({'Usuarios': lista_usuarios})
        
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            essential_fields = ['first_name', 'last_name', 'email', 'birth', 'phone_number', 'gender', 'images']
            generos = [genero[0] for genero in models.Profile.Genders]
            user_emails = User.objects.values_list('email', flat=True)


            if any(field not in data for field in essential_fields):
                return JsonResponse({'Informações Faltando': 'Campos obrigatórios não foram preenchidos'}, status=400)
            if data['email'] in user_emails:
                return JsonResponse({'Informações Invalidas': 'O email ja esta em uso'}, status=400)
            if data['gender'] not in generos:
                return JsonResponse({'Informações Invalidas': 'Por favor insira um genero valido'}, status=400)
            if data['password1'] != data['password2']:
                return JsonResponse({'Informações Incorretas': 'As senhas inseridas não são equivalentes'}, status=400)

            user = User.objects.create_user(username=data['email'], email=data['email'], password=data['password1'])
            user.save()
            profile = models.Profile.objects.create(
                user=user, first_name=data['first_name'], last_name=data['last_name'], email=data['email'], birth=data['birth'],
                phone_number=data['phone_number'], gender=data['gender'], images=data['images']
            )

            return JsonResponse({'mensagem': f'Usuario de id {profile.id} cadastrado com sucesso'}, status=201)
        
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
    
    

@csrf_exempt
def user_edit(request, id):
    try:
        print(request.method)
        if request.method == 'GET':
            user_profile = get_object_or_404(models.Profile, pk=id)
            resp = [{
                'id': user_profile.id,
                'first_name': user_profile.first_name,
                'last_name': user_profile.last_name,
                'email': user_profile.email,
                'birth': user_profile.birth,
                'phone_number': user_profile.phone_number,
                'gender': user_profile.gender,
                'date_joined': user_profile.date_joined,
                'last_acces': user_profile.last_acces,
                'user_type': user_profile.user_type,
                'images': user.images
            }]
            return JsonResponse({'Usuario': resp}, status=200)
        
        if request.method == 'PUT':
            user_profile = get_object_or_404(models.Profile, pk=id)
            user = get_object_or_404(User, pk=id)
            data = json.loads(request.body.decode('utf-8'))
            essential_fields = ['first_name', 'last_name', 'email', 'birth', 'phone_number', 'gender', 'images']
            generos = [genero[0] for genero in models.Profile.Genders]
            user_emails = User.objects.values_list('email', flat=True)

            if any(field not in data for field in essential_fields):
                return JsonResponse({'Informações Faltando': 'Campos obrigatórios não foram preenchidos'}, status=400)
            if data['email'] in user_emails:
                return JsonResponse({'Informações Invalidas': 'O email ja esta em uso'}, status=400)
            if data['gender'] not in generos:
                return JsonResponse({'Informações Invalidas': 'Por favor insira um genero valido'}, status=400)
            
            for field in vars(user_profile):
                if field in essential_fields:
                    setattr(user_profile, field, data[field])
                user_profile.save()
            user.username = data['email']
            user.email = data['email']
            user.save()

            return JsonResponse({"Usuario": f'Usuario de ID {id} editado com sucesso.'})

        if request.method == 'DELETE':
            user_profile = get_object_or_404(models.Profile, pk=id)
            user = get_object_or_404(User, pk=user_profile.user_id)
            user_profile.delete()
            user.delete()

            return JsonResponse({'Usuario': f"Usuario de ID {id} foi deletado"})
        
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
    
@csrf_exempt
def login(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            email = data['email']
            password = data['password']
            user = User.objects.get(email=email)

            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'Refresh': str(refresh),
                    'Authorization': str(refresh.access_token),
                })
            return JsonResponse({'Erro de Autenticação': "Verifique as credenciais informadas"}, status=500)

    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def teste(request):
    if request.user.is_authenticated:
        user = request.user
        user = get_object_or_404(models.Profile, email=user.email)

        user = user.id
        return JsonResponse({"Autenticado": user})
    return JsonResponse({"Falha de Autenticação": "Faça login para prosseguir"})