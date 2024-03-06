from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import Category, Product
from django.http import JsonResponse
from django.db import IntegrityError
import json


#REMOVER ANTES DE POSTAR
@csrf_exempt
#Funcao que faz os metodos post,get e delete para as categorias
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def categoria(request):
    try:
        if request.method == 'POST':
            if request.user.is_authenticated:
                user = request.user
                if user.is_superuser:
                    data = json.loads(request.body.decode('utf-8'))
                    nome = data.get('nome')  
                    if not nome:  
                        return JsonResponse({'erro': 'O campo nome é obrigatório'}, status=400)
                    Category.objects.create(name=nome) 
                    return JsonResponse({'mensagem': f'Categoria {nome} criada com sucesso'}, status=201)
                return JsonResponse({"Falha de Permissão": "Você não tem permissão de acesso à essa função"}, status=401)
            return JsonResponse({"Autorização Negada": "Faça login para prosseguir"}, status=401)

        elif request.method == 'GET':
            categorias = Category.objects.all()
            nomes_das_categorias = [categoria.name for categoria in categorias]
            return JsonResponse({'nomes': nomes_das_categorias}, status=200)
        
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
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def items(request):
    try:
        if request.method == 'POST':
            if request.user.is_authenticated:
                user = request.user
                if user.is_superuser:
                    data = json.loads(request.body.decode('utf-8'))

                    #Verifica valiez da informações
                    valido = verifica_validez_produto(data)
                    if valido == "Invalido por Categoria":
                        return JsonResponse({'Informações Invalidas': f'A categoria inserida não é valida.'}, status=400)
                    elif valido == "Invalido por Campos":
                        return JsonResponse({'Informações Faltando': 'Campos obrigatórios não foram preenchidos'}, status=400)

                    print(data['images'])
                    Product.objects.create(
                        name=data['nome'], description=data['descricao'], price=data['preco'], stock=data['estoque'],
                        total_sold=0, category=Category.objects.get(name=data['categoria']), images=data['images']
                    )

                    return JsonResponse({'mensagem': f'Produto {data["nome"]} criado com sucesso'}, status=201)
                return JsonResponse({"Falha de Permissão": "Você não tem permissão de acesso à essa função"}, status=401)
            return JsonResponse({"Autorização Negada": "Faça login para prosseguir"}, status=401)

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

            
            return JsonResponse({'produtos': lista_de_produtos}, status=200)

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
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
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
                'images': produto.images
            }
            return JsonResponse({'Produto': resp}, status=200)
        if request.user.is_authenticated:
            user = request.user
            if user.is_superuser:
                if request.method == 'PUT':
                    produto = Product.objects.get(id=id)
                    data = json.loads(request.body.decode('utf-8'))

                    #Verifica valiez da informações
                    valido = verifica_validez_produto(data)
                    if valido == "Invalido por Categoria":
                        return JsonResponse({'Informações Invalidas': f'A categoria inserida não é valida.'}, status=400)
                    elif valido == "Invalido por Campos":
                        return JsonResponse({'Informações Faltando': 'Campos obrigatórios não foram preenchidos'}, status=400)
                    
                    for field in vars(produto):
                        if field in data:
                            setattr(produto, field, data[field])
                        produto.save()
                    return JsonResponse({'Produto': f"Produto de ID {id} foi editado com sucesso"}, status=200)

                if request.method == 'DELETE':
                    produto = Product.objects.get(id=id)
                    produto.delete()
                    return JsonResponse({'Produto': f"Produto de ID {id} foi deletado"}, status=200)
            else:
                return JsonResponse({"Falha de Permissão": "Você não tem permissão de acesso à essa função"}, status=401)
        else:
            return JsonResponse({"Autorização Negada": "Faça login para prosseguir"}, status=401)



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