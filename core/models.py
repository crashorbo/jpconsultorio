from django.db import models
import datetime
# Create your models here.
class Movdiario(models.Model):
  fecha = models.DateField()
  ingreso = models.DecimalField(max_digits=10, decimal_places=2)
  egreso = models.DecimalField(max_digits=10, decimal_places=2)
  estado = models.BooleanField(default=True)

class MovMensual(models.Model):
  mes = models.IntegerField(default=0)
  gestion = models.IntegerField(default=2007)
  particular = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  seguro = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

class RecPaciente(models.Model):
  codigo = models.TextField(db_column='CODIGO', primary_key=True)  # Field name made lowercase.
  nombres = models.TextField(db_column='NOMBRES', blank=True, null=True)  # Field name made lowercase.
  a_paterno = models.TextField(db_column='A_PATERNO', blank=True, null=True)  # Field name made lowercase.
  a_materno = models.TextField(db_column='A_MATERNO', blank=True, null=True)  # Field name made lowercase.
  de = models.TextField(db_column='DE', blank=True, null=True)  # Field name made lowercase.
  fecha_nac = models.DateField(db_column='FECHA_NAC', blank=True, null=True)  # Field name made lowercase.
  direccion = models.TextField(db_column='DIRECCION', blank=True, null=True)  # Field name made lowercase.
  telefono = models.TextField(db_column='TELEFONO', blank=True, null=True)  # Field name made lowercase.
  ocupacion = models.TextField(db_column='OCUPACION', blank=True, null=True)  # Field name made lowercase.
  ci = models.TextField(db_column='CI', blank=True, null=True)  # Field name made lowercase.
  fecha_reg = models.DateField(db_column='FECHA_REG', blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'rec_paciente'

class RecHistoria(models.Model):
  codigo = models.TextField(db_column='CODIGO', primary_key=True)  # Field name made lowercase.
  paciente = models.TextField(db_column='PACIENTE', blank=True, null=True)  # Field name made lowercase.
  procedenc = models.TextField(db_column='PROCEDENC', blank=True, null=True)  # Field name made lowercase.
  oculares = models.TextField(db_column='OCULARES', blank=True, null=True)  # Field name made lowercase.
  sitemicos = models.TextField(db_column='SITEMICOS', blank=True, null=True)  # Field name made lowercase.
  mot_consul = models.TextField(db_column='MOT_CONSUL', blank=True, null=True)  # Field name made lowercase.
  av_od1 = models.TextField(db_column='AV_OD1', blank=True, null=True)  # Field name made lowercase.
  av_od2 = models.TextField(db_column='AV_OD2', blank=True, null=True)  # Field name made lowercase.
  av_od3a = models.TextField(db_column='AV_OD3A', blank=True, null=True)  # Field name made lowercase.
  av_od3b = models.TextField(db_column='AV_OD3B', blank=True, null=True)  # Field name made lowercase.
  av_od3c = models.TextField(db_column='AV_OD3C', blank=True, null=True)  # Field name made lowercase.
  av_od4 = models.TextField(db_column='AV_OD4', blank=True, null=True)  # Field name made lowercase.
  av_od5 = models.TextField(db_column='AV_OD5', blank=True, null=True)  # Field name made lowercase.
  av_od6 = models.TextField(db_column='AV_OD6', blank=True, null=True)  # Field name made lowercase.
  av_od7 = models.TextField(db_column='AV_OD7', blank=True, null=True)  # Field name made lowercase.
  av_od8 = models.TextField(db_column='AV_OD8', blank=True, null=True)  # Field name made lowercase.
  av_od9 = models.TextField(db_column='AV_OD9', blank=True, null=True)  # Field name made lowercase.
  av_od10a = models.TextField(db_column='AV_OD10A', blank=True, null=True)  # Field name made lowercase.
  av_od10b = models.TextField(db_column='AV_OD10B', blank=True, null=True)  # Field name made lowercase.
  av_od10c = models.TextField(db_column='AV_OD10C', blank=True, null=True)  # Field name made lowercase.
  av_oi1 = models.TextField(db_column='AV_OI1', blank=True, null=True)  # Field name made lowercase.
  av_oi2 = models.TextField(db_column='AV_OI2', blank=True, null=True)  # Field name made lowercase.
  av_oi3a = models.TextField(db_column='AV_OI3A', blank=True, null=True)  # Field name made lowercase.
  av_oi3b = models.TextField(db_column='AV_OI3B', blank=True, null=True)  # Field name made lowercase.
  av_oi3c = models.TextField(db_column='AV_OI3C', blank=True, null=True)  # Field name made lowercase.
  av_oi4 = models.TextField(db_column='AV_OI4', blank=True, null=True)  # Field name made lowercase.
  av_oi5 = models.TextField(db_column='AV_OI5', blank=True, null=True)  # Field name made lowercase.
  av_oi6 = models.TextField(db_column='AV_OI6', blank=True, null=True)  # Field name made lowercase.
  av_oi7 = models.TextField(db_column='AV_OI7', blank=True, null=True)  # Field name made lowercase.
  av_oi8 = models.TextField(db_column='AV_OI8', blank=True, null=True)  # Field name made lowercase.
  av_oi9 = models.TextField(db_column='AV_OI9', blank=True, null=True)  # Field name made lowercase.
  av_oi10a = models.TextField(db_column='AV_OI10A', blank=True, null=True)  # Field name made lowercase.
  av_oi10b = models.TextField(db_column='AV_OI10B', blank=True, null=True)  # Field name made lowercase.
  av_oi10c = models.TextField(db_column='AV_OI10C', blank=True, null=True)  # Field name made lowercase.
  adicion = models.TextField(db_column='ADICION', blank=True, null=True)  # Field name made lowercase.
  to_od = models.TextField(db_column='TO_OD', blank=True, null=True)  # Field name made lowercase.
  to_oi = models.TextField(db_column='TO_OI', blank=True, null=True)  # Field name made lowercase.
  biom_od = models.TextField(db_column='BIOM_OD', blank=True, null=True)  # Field name made lowercase.
  biom_oi = models.TextField(db_column='BIOM_OI', blank=True, null=True)  # Field name made lowercase.
  fondo_od = models.TextField(db_column='FONDO_OD', blank=True, null=True)  # Field name made lowercase.
  fondo_oi = models.TextField(db_column='FONDO_OI', blank=True, null=True)  # Field name made lowercase.
  otros = models.TextField(db_column='OTROS', blank=True, null=True)  # Field name made lowercase.
  fecha = models.DateField(db_column='FECHA', blank=True, null=True)  # Field name made lowercase.
  monto = models.FloatField(db_column='MONTO', blank=True, null=True)  # Field name made lowercase.
  eod = models.TextField(db_column='EOD', blank=True, null=True)  # Field name made lowercase.
  ciod = models.TextField(db_column='CIOD', blank=True, null=True)  # Field name made lowercase.
  ejeod = models.TextField(db_column='EJEOD', blank=True, null=True)  # Field name made lowercase.
  eoi = models.TextField(db_column='EOI', blank=True, null=True)  # Field name made lowercase.
  cioi = models.TextField(db_column='CIOI', blank=True, null=True)  # Field name made lowercase.
  ejeoi = models.TextField(db_column='EJEOI', blank=True, null=True)  # Field name made lowercase.
  dp1 = models.TextField(db_column='DP1', blank=True, null=True)  # Field name made lowercase.
  adicion1 = models.TextField(db_column='ADICION1', blank=True, null=True)  # Field name made lowercase.
  dp2 = models.TextField(db_column='DP2', blank=True, null=True)  # Field name made lowercase.
  otros1 = models.TextField(db_column='OTROS1', blank=True, null=True)  # Field name made lowercase.
  rec1 = models.TextField(db_column='REC1', blank=True, null=True)  # Field name made lowercase.
  rec2 = models.TextField(db_column='REC2', blank=True, null=True)  # Field name made lowercase.
  rec3 = models.TextField(db_column='REC3', blank=True, null=True)  # Field name made lowercase.
  rec4 = models.TextField(db_column='REC4', blank=True, null=True)  # Field name made lowercase.
  rec5 = models.TextField(db_column='REC5', blank=True, null=True)  # Field name made lowercase.
  rec6 = models.TextField(db_column='REC6', blank=True, null=True)  # Field name made lowercase.
  rec7 = models.TextField(db_column='REC7', blank=True, null=True)  # Field name made lowercase.
  rec8 = models.TextField(db_column='REC8', blank=True, null=True)  # Field name made lowercase.
  rec9 = models.TextField(db_column='REC9', blank=True, null=True)  # Field name made lowercase.
  rec10 = models.TextField(db_column='REC10', blank=True, null=True)  # Field name made lowercase.
  recet = models.TextField(db_column='RECET', blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'rec_historia'

class RecTratamiento(models.Model):
  cod = models.TextField(db_column='COD', primary_key=True)  # Field name made lowercase.
  detalle = models.TextField(db_column='DETALLE', blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'rec_tratamiento'

class RecDiagnostico(models.Model):
  cod = models.TextField(db_column='COD', primary_key=True)  # Field name made lowercase.
  detalle = models.TextField(db_column='DETALLE', blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'rec_diagnostico'