from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from paciente.models import Paciente
from seguro.models import Seguro
from servicio.models import Servicio


class Agenda(models.Model):
  TIPO_CHOICE = (
    (0, 'PARTICULAR'),
    (1, 'SEGURO'),
  )

  PRIORIDAD_CHOICE = (
    (0, 'LEVE'),
    (1, 'MODERADO'),
    (2, 'URGENTE'),
  )
  DECERCA_CHOICE = (
    ('J1', 'J1'),
    ('J2', 'J2'),
    ('J3', 'J3'),
    ('J4', 'J4'),
    ('J5', 'J5'),
  )

  BENEFICIARIO_CHOICE = (
    (0, 'BENF'),
    (1, 'ACT'),
    (2, 'RENT'),
  )

  paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
  seguro = models.ForeignKey(Seguro, on_delete=models.CASCADE)
  fecha = models.DateField(default=datetime.now)
  hora_inicio = models.TimeField(default=datetime.now())
  hora_fin = models.TimeField(default=datetime.now(), blank=True)
  estado = models.IntegerField(default=0)
  prioridad = models.IntegerField(choices=PRIORIDAD_CHOICE,default=0)
  tipo = models.IntegerField(choices=TIPO_CHOICE, default=0)
  procedencia = models.CharField(max_length=20, blank=True)
  matricula = models.CharField(max_length=100, blank=True)
  tipo_beneficiario = models.IntegerField(choices=BENEFICIARIO_CHOICE, default=0)
  antocu = models.TextField(blank=True)
  antsis = models.TextField(blank=True)
  motivo = models.TextField(blank=True)
  dsc = models.CharField(max_length=50, blank=True)
  dcc = models.CharField(max_length=50, blank=True)
  dre1 = models.CharField(max_length=50, blank=True)
  dre2 = models.CharField(max_length=50, blank=True)
  dre3 = models.CharField(max_length=50, blank=True)
  dau = models.CharField(max_length=50, blank=True)
  ddc1 = models.CharField(max_length=50, blank=True, choices=DECERCA_CHOICE)
  ddc2 = models.CharField(max_length=50, blank=True)
  dph = models.CharField(max_length=50, blank=True)
  dci = models.CharField(max_length=50, blank=True)
  dcl = models.CharField(max_length=50, blank=True)
  drc1 = models.CharField(max_length=50, blank=True)
  drc2 = models.CharField(max_length=50, blank=True)
  drc3 = models.CharField(max_length=50, blank=True)
  isc = models.CharField(max_length=50, blank=True)
  icc = models.CharField(max_length=50, blank=True)
  ire1 = models.CharField(max_length=50, blank=True)
  ire2 = models.CharField(max_length=50, blank=True)
  ire3 = models.CharField(max_length=50, blank=True)
  iau = models.CharField(max_length=50, blank=True)
  idc1 = models.CharField(max_length=50, blank=True, choices=DECERCA_CHOICE)
  idc2 = models.CharField(max_length=50, blank=True)
  iph = models.CharField(max_length=50, blank=True)
  ici = models.CharField(max_length=50, blank=True)
  icl = models.CharField(max_length=50, blank=True)
  irc1 = models.CharField(max_length=50, blank=True)
  irc2 = models.CharField(max_length=50, blank=True)
  irc3 = models.CharField(max_length=50, blank=True)
  adicion = models.CharField(max_length=100, blank=True)
  dto = models.CharField(max_length=50, blank=True)
  ito = models.CharField(max_length=50, blank=True)
  dbio = models.TextField(blank=True)
  ibio = models.TextField(blank=True)
  dfdo = models.TextField(blank=True)
  ifdo = models.TextField(blank=True)
  otros = models.TextField(blank=True)
  tipo_lente = models.TextField(blank=True)

  def __str__(self):
    return self.fecha.strftime('%d/%m/%Y')

  class Meta:
    ordering = ('fecha',)


class Diagnostico(models.Model):
  agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
  detalle = models.CharField(max_length=200)

class Tratamiento(models.Model):
  agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
  detalle = models.CharField(max_length=200)


class Agendaserv(models.Model):
  agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
  servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
  costo = models.DecimalField(max_digits=5, decimal_places=2)
  fecha = models.DateField(default=timezone.now)
  hora = models.DateTimeField(default=timezone.now)
  estado = models.BooleanField(default=False)