from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from . import models
import json


#REMOVER ANTES DE POSTAR
@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def evento(request):
    try:
        if request.method == 'POST':
            if request.user.is_authenticated:
                user = request.user
                if user.is_superuser:
                    data = json.loads(request.body.decode('utf-8'))
                    obrigatory_fields = ['name', 'location', 'description', 'date', 'people', 'sponsors', 'images']
                    if any(field not in data for field in obrigatory_fields):
                        return JsonResponse({'Informações Faltando': 'Campos obrigatórios não foram preenchidos'}, status=400)
                    models.Event.objects.create(name=data['name'], location=data['location'], description=data['description'], date=data['date'], people=data['people'], sponsors=data['sponsors'], images=data['images'])
                   
                    return JsonResponse({'Success': 'Event created sucessfully'}, status=201)
                return JsonResponse({"Falha de Permissão": "Você não tem permissão de acesso à essa função"}, status=401)
            return JsonResponse({"Autorização Negada": "Faça login para prosseguir"}, status=401)
        
        if request.method == 'GET':
            list_events = []
            events = models.Event.objects.all()
            for event in events:
                list_events.append({
                  'id': event.id, 'name': event.name, 'location': event.location, 'description': event.description, 'date': event.date, 'people': event.people, 'sponsors': event.sponsors, 'images': event.images  
                })
            list_events = sorted(list_events, key=lambda x: x['id'])
            return JsonResponse({'Eventos': list_events}, status=200)

    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def unique(request, id):
    try:
        if request.method == 'GET':
            event = get_object_or_404(models.Event, pk=id)
            resp = {
                  'id': event.id, 'name': event.name, 'location': event.location, 'description': event.description, 'date': event.date, 'people': event.people, 'sponsors': event.sponsors, 'images': event.images  
                }
            return JsonResponse({'Evento': resp}, status=200)
        
        if request.method in ['DELETE', 'PUT']:
            if request.user.is_authenticated:
                user = request.user
                if user.is_superuser:
                    if request.method == 'DELETE':
                        event = models.Event.objects.get(id=id)
                        event.delete()
                        return JsonResponse({'Evento': f"Evento de ID {id} foi deletado"}, status=200)
                    
                    if request.method == 'PUT':
                        event = models.Event.objects.get(id=id)
                        data = json.loads(request.body.decode('utf-8'))
                        obrigatory_fields = ['name', 'location', 'description', 'date', 'people', 'sponsors', 'images']
                        if any(field not in data for field in obrigatory_fields):
                            return JsonResponse({'Informações Faltando': 'Campos obrigatórios não foram preenchidos'}, status=400)
                        for field in vars(event):
                            if field in obrigatory_fields:
                                setattr(event, field, data[field])
                            event.save()

                        return JsonResponse({'Evento': f"Evento de id {id} foi alterado"}, status=200)
                return JsonResponse({"Falha de Permissão": "Você não tem permissão de acesso à essa função"}, status=401)
            return JsonResponse({"Autorização Negada": "Faça login para prosseguir"}, status=401)

    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)