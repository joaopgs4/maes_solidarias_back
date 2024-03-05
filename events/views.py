from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import models
import json
from django.db import IntegrityError

#REMOVER ANTES DE POSTAR
@csrf_exempt
def evento(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            obrigatory_fields = ['name', 'location', 'description', 'date', 'people', 'sponsors']
            if any(field not in data for field in obrigatory_fields):
                return JsonResponse({'Informações Faltando': 'Campos obrigatórios não foram preenchidos'}, status=400)
            models.Event.objects.create(name=data['name'], location=data['location'], description=data['description'], date=data['date'], people=data['people'], sponsors=data['sponsors'])
            return JsonResponse({'Success': 'Event created sucessfully'}, status=201)
        
        if request.method == 'GET':
            list_events = []
            events = models.Event.objects.all()
            for event in events:
                list_events.append({
                  'id': event.id, 'name': event.name, 'location': event.location, 'description': event.description, 'date': event.date, 'people': event.people, 'sponsors': event.sponsors  
                })
            list_events = sorted(list_events, key=lambda x: x['id'])
            return JsonResponse({'Eventos': list_events})

    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)

@csrf_exempt
def unique(request, id):
    try:
        if request.method == 'GET':
            event = get_object_or_404(models.Event, pk=id)
            resp = {
                  'id': event.id, 'name': event.name, 'location': event.location, 'description': event.description, 'date': event.date, 'people': event.people, 'sponsors': event.sponsors  
                }
            return JsonResponse({'Evento': resp})
        
        if request.method == 'DELETE':
            event = models.Event.objects.get(id=id)
            event.delete()
            return JsonResponse({'Evento': f"Evento de ID {id} foi deletado"})
        
        if request.method == 'PUT':
            event = models.Event.objects.get(id=id)
            data = json.loads(request.body.decode('utf-8'))
            obrigatory_fields = ['name', 'location', 'description', 'date', 'people', 'sponsors']
            if any(field not in data for field in obrigatory_fields):
                return JsonResponse({'Informações Faltando': 'Campos obrigatórios não foram preenchidos'})
            for field in vars(event):
                if field in obrigatory_fields:
                    setattr(event, field, data[field])
                event.save()

            return JsonResponse({'Evento': f"Evento de id {id} foi alterado"})

    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)