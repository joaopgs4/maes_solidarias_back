from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name', 'name')
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    stock = models.IntegerField()
    total_sold = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="store_products", blank=True, null=True)

    #Foreign keys
    #Como python não é uma linguagem compilada, para referir a uma classe precisamos chama-la após a criação. Por isso Produto vem depois de Categoria
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE) 