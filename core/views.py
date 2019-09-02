from django.shortcuts import render
from django.views.generic import TemplateView, View
from datetime import datetime
from django.http import HttpResponse,JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder

from .models import Movdiario
from servicio.models import Servicio
from seguro.models import Segurocosto
from agenda.models import Agenda
# Create your views here.


# Vista Inicial de la aplicacion
class IndexView(TemplateView):
    template_name = 'core/index.html'

class MovimientoCalculoView(View):
    def get(self, *args, **kwargs):
        hoy = datetime.now()
        fecha = hoy.strftime("%Y-%m-%d")
        try:
            movimiento = Movdiario.objects.get(fecha=datetime.strptime(fecha, "%Y-%m-%d"))
        except Movdiario.DoesNotExist:
            movimiento = Movdiario(fecha=datetime.strptime(fecha, "%Y-%m-%d"), ingreso=0, egreso=0, estado=True)
        movimiento = self.get_results(movimiento)
        return HttpResponse( json.dumps(movimiento, cls=DjangoJSONEncoder), content_type='application/json')
    
    def get_results(self, x):
        return dict(fecha=x.fecha.strftime("%Y-%m-%d" ),ingreso=x.ingreso, egreso=x.egreso, estado=x.estado)

class ServicioCostoView(View):
    def get(self, *args, **kwargs):        
        servicio = Servicio.objects.get(id=self.request.GET['id'])
        return JsonResponse({"success": True, "costo": servicio.costo})

class ServicioSeguroCosto(View):
    def get(self, *args, **kwargs):
        segurocosto = Segurocosto.objects.get(seguro=self.request.GET['seguro'], servicio=self.request.GET['servicio'])
        return JsonResponse({"success": True, "costo": segurocosto.costo})

class GraficoView(View):
    def get(self, *args, **kwargs):
        now = datetime.now()
        particular = []
        seguro = []
        for i in range(12):
            particular.append(Agenda.objects.filter(fecha__year=now.year, fecha__month=i+1, tipo=0, estado=1).count())
            seguro.append(Agenda.objects.filter(fecha__year=now.year, fecha__month=i+1, tipo=1, estado=1).count())
        grafico = {"particular": particular, "seguro": seguro}
        return HttpResponse( json.dumps(grafico, cls=DjangoJSONEncoder), content_type='application/json')

class GraficoFechaView(View):
    def get(self, *args, **kwargs):
        year = self.kwargs['year']
        particular = []
        seguro = []
        for i in range(12):
            particular.append(Agenda.objects.filter(fecha__year=year, fecha__month=i + 1, tipo=0, estado=1).count())
            seguro.append(Agenda.objects.filter(fecha__year=year, fecha__month=i + 1, tipo=1, estado=1).count())
        grafico = {"particular": particular, "seguro": seguro}
        return HttpResponse(json.dumps(grafico, cls=DjangoJSONEncoder), content_type='application/json')