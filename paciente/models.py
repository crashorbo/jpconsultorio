from django.db import models
from uuid import uuid4
from datetime import date, datetime
import os
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.

class MyModelMixin(object):

  def q_for_search_word(self, word):
    return Q(nombres__icontains=word) | Q(apellidos__icontains=word) | Q(documento__icontains=word) | Q(nro_documento__icontains=word) | Q(telefono__icontains=word)

  def q_for_search(self, search):
    q = Q()
    if search:
        searches = search.split()
        for word in searches:
            q = q & self.q_for_search_word(word)
    return q

  def filter_on_search(self, search):
    return self.filter(self.q_for_search(search))

class MyModelQuerySet(QuerySet, MyModelMixin):
  pass

class MyModelManager(models.Manager, MyModelMixin):
  
  def get_queryset(self):
    return MyModelQuerySet(self.model, using=self._db)

class Paciente(models.Model):
  DOCUMENTO_CHOICE = (
    (1, 'CEDULA DE IDENTIDAD'),
    (2, 'PASAPORTE'),
    (3, 'CERTIFICADO DE NACIMIENTO')
  )

  DOCUMENTO_PRINT = {
    1: 'CEDULA DE IDENTIDAD',
    2: 'PASAPORTE',
    3: 'CERTIFICADO DE NACIMIENTO'
  }

  nombres = models.CharField(max_length=100)
  apellidos = models.CharField(max_length=100)
  fecha_nacimiento = models.DateField(default=datetime.now)
  documento = models.IntegerField(choices=DOCUMENTO_CHOICE, default=1)
  nro_documento = models.CharField(max_length=20, blank=True)
  direccion = models.TextField(blank=True)
  telefono = models.CharField(max_length=20, blank=True)
  ocupacion = models.CharField(max_length=50, blank=True)
  codigo = models.TextField(blank=True)
  creado = models.DateTimeField(auto_now=True)
  estado = models.BooleanField(default=True)
  objects = MyModelManager()

  def __str__(self):
    return self.nombres+' '+self.apellidos+' - '+self.nro_documento
  
  def as_list(self):
    return [self.nombres+' '+self.apellidos,
      self.DOCUMENTO_PRINT[self.documento],
      self.nro_documento,
      self.telefono,
      self.codigo,
      '<button class="paciente-historial btn btn-xs btn-info" data-url='+reverse('historia-lista',args=[self.id])+'><i class="icon-medical-history"></i></button><button class="paciente-examen btn btn-xs btn-success m-l-5" data-url='+reverse('archivopdf-listar',args=[self.id])+'><i class="fa fa-file-pdf-o"></i></button><button class="paciente-editar btn btn-xs btn-warning m-l-5" data-url='+reverse('paciente-editar', args=[self.id])+'><i class="fa fa-edit"></i></button>']

class Archivopdf(models.Model):
  def _generar_ruta_archivo(instance, filename):
    # El primer paso es extraer la extension de la imagen del
    # archivo original
    extension = os.path.splitext(filename)[1][1:]

    # Generamos la ruta relativa a MEDIA_ROOT donde almacenar
    # el archivo, usando la fecha actual (año/mes)
    ruta = os.path.join('Documentos', date.today().strftime("%Y/%m"))

    # Generamos el nombre del archivo con un identificador
    # aleatorio, y la extension del archivo original.
    nombre_archivo = '{}.{}'.format(uuid4().hex, extension)

    # Devolvermos la ruta completa
    return os.path.join(ruta, nombre_archivo)

  paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
  fecha = models.DateField(auto_now=True)
  fecha_documento = models.DateField(default=datetime.now)
  archivo = models.FileField(upload_to=_generar_ruta_archivo, blank=True)
  nombre = models.CharField(max_length=200, blank=True)
  #descripcion = models.TextField(blank=True)
  descripcion = RichTextField(blank=True)
  estado = models.BooleanField(default=True)

class Nota(models.Model):
  TIPO_CHOICES = (
    (0, "NOTA"),
    (1, "EXAMEN EXTERNO"),
    (2, "CERTIFICADO MEDICO"),
  )
  paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
  tipo = models.IntegerField(default=0, choices=TIPO_CHOICES)
  fecha = models.DateField(auto_now=True)
  fecha_documento = models.DateField(default=datetime.now)
  nombre = models.CharField(max_length=200, blank=True)
  texto = models.TextField(blank=True)
  estado = models.BooleanField(default=True)