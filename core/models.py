from django.db import models

# Create your models here.
class Movdiario(models.Model):
  fecha = models.DateField()
  ingreso = models.DecimalField(max_digits=10, decimal_places=2)
  egreso = models.DecimalField(max_digits=10, decimal_places=2)
  estado = models.BooleanField(default=True)