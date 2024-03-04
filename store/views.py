from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Product
import json
from django.db import IntegrityError

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

#funcao que adiciona, deleta, atualiza e lista os produtos
@csrf_exempt
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
            if not descricao:
                return JsonResponse({'erro': 'O campo descricao é obrigatório'}, status=400)
            if not preco:
                return JsonResponse({'erro': 'O campo preco é obrigatório'}, status=400)
            if estoque is None:
                return JsonResponse({'erro': 'O campo estoque é obrigatório'}, status=400)
            category = Category.objects.get(name=categoria)

            produto = Product.objects.create(
                name=nome, description=descricao, price=preco, stock=estoque,
                total_sold=total_vendido, category=category
            )

            return JsonResponse({'mensagem': 'Produto criado com sucesso'}, status=201)

        elif request.method == 'GET':
            produtos = Product.objects.all()
            
            lista_de_produtos = [{
                'nome': produto.name,
                'descricao': produto.description,
                'preco': produto.price,
                'estoque': produto.stock,
                'total_vendido': produto.total_sold,
                'categoria': produto.category.name
            } for produto in produtos]
            
            return JsonResponse({'produtos': lista_de_produtos})

        elif request.method == 'DELETE':
            data = json.loads(request.body.decode('utf-8'))
            nome = data.get('nome')
            produto = Product.objects.get(name=nome)
            produto.delete()
            return JsonResponse({'mensagem': 'Produto deletado com sucesso'}, status=200)
        elif request.method == 'PUT':
                data = json.loads(request.body.decode('utf-8'))
                nome = data.get('nome')
                
                # Verificar se o produto existe
                produto = Product.objects.get(name=nome)
                
                # Atualizar os campos com os dados fornecidos, se estiverem presentes na requisição
                descricao = data.get('descricao')
                if descricao is not None:
                    produto.description = descricao
                novo_nome = data.get('novo_nome')
                if novo_nome is not None:
                    produto.name = novo_nome
                
                preco = data.get('preco')
                if preco is not None:
                    produto.price = preco
                
                estoque = data.get('estoque')
                if estoque is not None:
                    produto.stock = estoque
                
                total_vendido = data.get('total_vendido')
                if total_vendido is not None:
                    produto.total_sold = total_vendido
                
                categoria = data.get('categoria')
                if categoria is not None:
                    produto.category = Category.objects.get(name=categoria)
                produto.save()
                return JsonResponse({'mensagem': 'Produto atualizado com sucesso'}, status=200)
    except Product.DoesNotExist:
        return JsonResponse({'erro': 'Produto não encontrado'}, status=404)
    except Category.DoesNotExist:
        return JsonResponse({'erro': 'Categoria não encontrada'}, status=404)
    except IntegrityError:
        return JsonResponse({'erro': 'Formato de JSON inválido'}, status=400)
    except KeyError as e:
        return JsonResponse({'erro': f'Campo {e} faltando'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
