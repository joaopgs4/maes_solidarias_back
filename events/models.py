from django.db import models
# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    people = models.IntegerField()
    image = models.ImageField(upload_to="events", blank=True, null=True)
    sponsors = models.TextField()

    class Meta:
        ordering = ('name', 'name')

    def __str__(self):
        return self.name