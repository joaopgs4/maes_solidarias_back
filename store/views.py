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
            return JsonResponse({'mensagem': f'Categoria {nome} criada com sucesso'}, status=201)
        
        elif request.method == 'GET':
            categorias = Category.objects.all()
            nomes_das_categorias = [categoria.name for categoria in categorias]
            return JsonResponse({'nomes': nomes_das_categorias})
        
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

            #Verifica valiez da informações
            valido = verifica_validez_produto(data)
            if valido == "Invalido por Categoria":
                return JsonResponse({'Informações Invalidas': f'A categoria inserida não é valida.'})
            elif valido == "Invalido por Campos":
                return JsonResponse({'Informações Faltando': 'Campos obrigatórios não foram preenchidos'}, status=400)

            print(data['images'])
            Product.objects.create(
                name=data['nome'], description=data['descricao'], price=data['preco'], stock=data['estoque'],
                total_sold=0, category=Category.objects.get(name=data['categoria']), images=data['images']
            )

            return JsonResponse({'mensagem': f'Produto {data["nome"]} criado com sucesso'}, status=201)

        elif request.method == 'GET':
            produtos = Product.objects.all()
            
            lista_de_produtos = [{
                'id': produto.id,
                'nome': produto.name,
                'descricao': produto.description,
                'preco': produto.price,
                'estoque': produto.stock,
                'total_vendido': produto.total_sold,
                'categoria': produto.category.name,
                'images': produto.images
            } for produto in produtos]
            lista_de_produtos = sorted(lista_de_produtos, key=lambda x: x['id'])

            
            return JsonResponse({'produtos': lista_de_produtos})

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

@csrf_exempt
def items_id(request, id):
    try:
        if request.method == 'GET':
            produto = Product.objects.get(id=id)
            resp = {
                'id': produto.id,
                'nome': produto.name,
                'descricao': produto.description,
                'preco': produto.price,
                'estoque': produto.stock,
                'total_vendido': produto.total_sold,
                'categoria': produto.category.name,
                'images': produto.image
            }
            return JsonResponse({'Produto': resp})
        
        if request.method == 'PUT':
            produto = Product.objects.get(id=id)
            data = json.loads(request.body.decode('utf-8'))

            #Verifica valiez da informações
            valido = verifica_validez_produto(data)
            if valido == "Invalido por Categoria":
                return JsonResponse({'Informações Invalidas': f'A categoria inserida não é valida.'})
            elif valido == "Invalido por Campos":
                return JsonResponse({'Informações Faltando': 'Campos obrigatórios não foram preenchidos'}, status=400)
            
            for field in vars(produto):
                if field in data:
                    setattr(produto, field, data[field])
                produto.save()
            return JsonResponse({'Produto': f"Produto de ID {id} foi editado com sucesso"})

        if request.method == 'DELETE':
            produto = Product.objects.get(id=id)
            produto.delete()
            return JsonResponse({'Produto': f"Produto de ID {id} foi deletado"})


    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
        

#Função auxiliar para deixar o código mais clean
def verifica_validez_produto(data):
    obrigatory_fields = ['nome', 'descricao', 'preco', 'estoque', 'categoria', 'images']
    if any(field not in data for field in obrigatory_fields):
        return "Invalido por Campos"

    categorias = Category.objects.all()
    nomes_das_categorias = [categoria.name for categoria in categorias]
    if data['categoria'] not in nomes_das_categorias:
        return "Invalido por Categoria"