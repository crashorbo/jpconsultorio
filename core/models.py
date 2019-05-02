from django.db import models

# Create your models here.
class Movdiario(models.Model):
  fecha = models.DateField()
  ingreso = models.DecimalField(max_digits=10, decimal_places=2)
  egreso = models.DecimalField(max_digits=10, decimal_places=2)
  estado = models.BooleanField(default=True)

class Recpaciente(models.Model):
  codigo = models.TextField(primary_key=True)
  nombres = models.TextField(blank=True, null=True)
  a_paterno = models.TextField(blank=True, null=True)
  a_materno = models.TextField(blank=True, null=True)
  de = models.TextField(blank=True, null=True)
  fecha_nac = models.DateField(blank=True, null=True)
  direccion = models.TextField(blank=True, null=True)
  telefono = models.TextField(blank=True, null=True)
  ocupacion = models.TextField(blank=True, null=True)
  ci = models.TextField(blank=True, null=True)
  fecha_reg = models.DateField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'rec_paciente'