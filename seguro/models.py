from django.db import models

# Create your models here.
class Seguro(models.Model):
  nombre = models.CharField(max_length=200)
  direccion = models.TextField(blank=True)
  telefono = models.CharField(max_length=20, blank=True)

  def __str__(self):
    return self.nombre

  class Meta:
    ordering = ('nombre',)

