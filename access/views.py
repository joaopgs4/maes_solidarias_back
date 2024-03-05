from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Profile
import json


#REMOVER ANTES DE POSTAR
@csrf_exempt
def usuario(request):
    try:

        # CADASTRA USUARIO
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            birth = data.get('birth')
            phone_number = data.get('phone_number')
            gender = data.get('gender')
            
            if not first_name:
                return JsonResponse({'erro': 'O campo first_name é obrigatório'}, status=400)
            if not last_name:
                return JsonResponse({'erro': 'O campo last_name é obrigatório'}, status=400)
            if not email:
                return JsonResponse({'erro': 'O campo email é obrigatório'}, status=400)
            if not birth:
                return JsonResponse({'erro': 'O campo birth é obrigatório'}, status=400)
            if not phone_number:
                return JsonResponse({'erro': 'O campo phone_number é obrigatório'}, status=400)
            if not gender:
                return JsonResponse({'erro': 'O campo gender é obrigatório'}, status=400)

            Profile.objects.create(
                first_name=first_name, last_name=last_name, email=email, birth=birth,
                phone_number=phone_number, gender=gender
            )

            return JsonResponse({'mensagem': 'Usuario cadastrado com sucesso'}, status=201)
        
        # DELETA USUARIO
        elif request.method == 'DELETE':
            data = json.loads(request.body.decode('utf-8'))
            user = data.get('user')
            profile = Profile.objects.get(user=user)
            profile.delete()
            return JsonResponse({'mensagem': 'Usuario deletado com sucesso'}, status=200)

        # EDITA USUARIO (SOMENTE PARA ADM)
        elif request.method == 'PUT':
            data = json.loads(request.body.decode('utf-8'))
            user = data.get('user')
            profile = Profile.objects.get(user=user)

            new_user_type = data.get('user_type')
            profile.user_type = new_user_type
            profile.save()
            return JsonResponse({'mensagem': 'Usuario editado com sucesso'}, status=200)

        elif request.method == 'GET':
            usuarios = Profile.objects.all()
            
            lista_usuarios = [{
                'user': usuario.user,
                'first_name': usuario.first_name,
                'last_name': usuario.last_name,
                'email': usuario.email,
                'birth': usuario.birth,
                'phone_number': usuario.phone_number,
                'gender': usuario.gender,
                'date_joined': usuario.date_joined,
                'last_acces': usuario.last_acces,
                'profile_img': usuario.profile_img
            } for usuario in usuarios]
            
            return JsonResponse({'usuarios': lista_usuarios})


    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
    
