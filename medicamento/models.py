from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.db.models.query import QuerySet

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

class Medicamento(models.Model):
  PRESENTACION_CHOICE = (
    (1,'Solucion'),
    (2,'Jarabe'),
    (3,'Colirio'),
    (4,'Locion'),
    (5,'Linimento'),
    (6,'Ovulo'),
    (7,'Pomada'),
    (8,'Crema'),
    (9,'Capsula'),
    (10,'Comprimido'),
    (11,'Pildora'),
    (12,'Gragea'),
    (13,'Polvo'),
    (14,'Supositorio'),    
  )

  PRESENTACION_PRINT = {
    1:'Solucion',
    2:'Jarabe',
    3:'Colirio',
    4:'Locion',
    5:'Linimento',
    6:'Ovulo',
    7:'Pomada',
    8:'Crema',
    9:'Capsula',
    10:'Comprimido',
    11:'Pildora',
    12:'Gragea',
    13:'Polvo',
    14:'Supositorio',    
  }

  nombre = models.CharField(max_length=200, blank=True)
  presentacion = models.IntegerField(choices=PRESENTACION_CHOICE, default=1)
  indicacion = models.TextField(blank=True)

  objects = MyModelManager()

  def __str__(self):
    return self.nombre+' - '+self.PRESENTACION_PRINT[self.presentacion]

  def as_list(self):
    return [self.nombre,            
            self.PRESENTACION_PRINT[self.presentacion],
            self.indicacion,
            '<button class="medicamento-editar btn btn-xs btn-warning m-l-5" data-url='+reverse('medicamento-ajax-editar', args=[self.id])+'><i class="fa fa-edit"></i></button><button class="medicamento-eliminar btn btn-xs btn-danger m-l-5" data-url='+str(self.id)+'><i class="fa fa-close"></i></button>']