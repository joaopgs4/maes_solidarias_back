from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import Category
import json
@csrf_exempt
def categoria(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            nome = data.get('nome')  
            if not nome:  
                return JsonResponse({'erro': 'O campo nome é obrigatório'}, status=400)
            Category.objects.create(name=nome) 
            return JsonResponse({'mensagem': 'Categoria criada com sucesso'}, status=201)
        
        elif request.method == 'GET':
            categorias = Category.objects.all()
            nomes_das_categorias = [categoria.name for categoria in categorias]
            return JsonResponse({'nomes': nomes_das_categorias})
        
        elif request.method == 'DELETE':
            data = json.loads(request.body.decode('utf-8'))
            nome = data.get('nome')
            categoria = Category.objects.get(name=nome)
            categoria.delete()
            return JsonResponse({'mensagem': 'Categoria deletada com sucesso'}, status=200)
        
    except Category.DoesNotExist:
        return JsonResponse({'erro': 'Categoria não encontrada'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'Formato de JSON inválido'}, status=400)
    except KeyError as e:
        return JsonResponse({'erro': f'Campo {e} faltando'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)