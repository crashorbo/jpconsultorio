from django.shortcuts import render
from django.views.generic import TemplateView, View
from datetime import datetime
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder

from .models import Movdiario
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