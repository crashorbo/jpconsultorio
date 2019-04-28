from django.db import models

# Create your models here.
class Servicio(models.Model):
  nombre = models.CharField(max_length=200)
  costo = models.DecimalField(max_digits=5, decimal_places=2)

  def __str__(self):
    return self.nombre

  class Meta:
    ordering = ('nombre',)