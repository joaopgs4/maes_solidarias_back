from django.db import models

# Cria o modelo de evento, as imagens estão como text_field para salvar em base x64 por eficiencia
class Event(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    people = models.IntegerField()
    images = models.TextField(blank=True, null=True)
    sponsors = models.TextField()

    class Meta:
        ordering = ('name', 'name')

    def __str__(self):
        return self.name