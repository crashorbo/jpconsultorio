from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet

from seguro.models import Seguro

# Create your models here.

MESES_CHOICES = (
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre'),
    )


class Reportegeneral(models.Model):
    mes = models.IntegerField(default=1, choices=MESES_CHOICES)
    gestion = models.IntegerField(default=0)
    particular = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seguro = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gestion + self.mes


class Reporteseguro(models.Model):
    seguro = models.ForeignKey(Seguro, on_delete=models.CASCADE)
    mes = models.IntegerField(default=1, choices=MESES_CHOICES)
    gestion = models.IntegerField(default=0)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gestion + self.mes
