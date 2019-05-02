from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
# Create your models here.

class Paciente(models.Model):
  DOCUMENTO_CHOICE = (
    (1, 'CEDULA DE IDENTIDAD'),
    (2, 'PASAPORTE'),
    (3, 'CERTIFICADO DE NACIMIENTO')
  )

  nombres = models.CharField(max_length=100)
  apellidos = models.CharField(max_length=100)
  fecha_nacimiento = models.DateField(default=datetime.datetime.now)
  documento = models.IntegerField(choices=DOCUMENTO_CHOICE, default=1)
  nro_documento = models.CharField(max_length=20, blank=True)
  direccion = models.TextField(blank=True)
  telefono = models.CharField(max_length=20, blank=True)
  ocupacion = models.CharField(max_length=50, blank=True)
  codigo = models.TextField(blank=True)
  creado = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.nombres+' '+self.apellidos+' - '+self.nro_documento
  def get_absolute_url(self):
    return ('/paciente')