from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import Category
@csrf_exempt
def categoria(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        categoria = Category(name=nome)
        categoria.save()
        return render(request, 'store/add_category.html', {'categoria': categoria})
    if request.method == 'GET':
        return 
