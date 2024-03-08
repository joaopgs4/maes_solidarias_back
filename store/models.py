from django.db import models

# Criação de modelos de objetos utilizados na loja

# Um simples modelo de categoria, que armazena a categoria de um produto utilizando uma Foreign Key
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name', 'name')
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name

# Define um produto, tal como todas as suas informações padrões.
#Como python não é uma linguagem compilada, para referir a uma classe precisamos chama-la após a criação. Por isso Produto vem depois de Categoria
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    stock = models.IntegerField()
    total_sold = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    images = models.TextField(blank=True, null=True)

    #Foreign keys
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE) 