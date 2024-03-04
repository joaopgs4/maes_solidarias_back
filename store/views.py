from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Product
import json

#REMOVER ANTES DE POSTAR
@csrf_exempt

#Funcao que faz os metodos post,get e delete para as categorias
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
    
def items(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            nome = data.get('nome')
            descricao = data.get('descricao')
            preco = data.get('preco')
            estoque = data.get('estoque')
            total_vendido = data.get('total_vendido')
            categoria = data.get('categoria')
            if not nome:
                return JsonResponse({'erro': 'O campo nome é obrigatório'}, status=400)
            if not preco:
                return JsonResponse({'erro': 'O campo preco é obrigatório'}, status=400)
            if not estoque:
                return JsonResponse({'erro': 'O campo estoque é obrigatório'}, status=400)
            if not total_vendido:
                return JsonResponse({'erro': 'O campo total_vendido é obrigatório'}, status=400)
            if not categoria:
                return JsonResponse({'erro': 'O campo categoria é obrigatório'}, status=400)
            category = Category.objects.get(name=categoria)
            Product.objects.create(name=nome, description=descricao, price=preco, stock=estoque, total_sold=total_vendido, category=category)
            return JsonResponse({'mensagem': 'Produto criado com sucesso'}, status=201)
        
        elif request.method == 'GET':
            produtos = Product.objects.all()
            nomes_dos_produtos = [produto.name for produto in produtos]
            return JsonResponse({'nomes': nomes_dos_produtos})
        
        elif request.method == 'DELETE':
            data = json.loads(request.body.decode('utf-8'))
            nome = data.get('nome')
            produto = Product.objects.get(name=nome)
            produto.delete()
            return JsonResponse({'mensagem': 'Produto deletado com sucesso'}, status=200)
        
    except Product.DoesNotExist:
        return JsonResponse({'erro': 'Produto não encontrado'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'Formato de JSON inválido'}, status=400)
    except KeyError as e:
        return JsonResponse({'erro': f'Campo {e} faltando'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)