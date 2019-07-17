from django.shortcuts import render
from django.views.generic import ListView, View, UpdateView, CreateView, TemplateView
from braces.views import JSONResponseMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render
from dal import autocomplete
from django.db.models import Q

from .models import Medicamento
from .forms import MedicamentoForm

# Create your views here.
class TableAsJSON(JSONResponseMixin, View):
  model = Medicamento

  def get(self, request, *args, **kwargs):
    col_name_map = {
      '0': 'nombre',
      '1': 'presentacion',
      '2': 'indicacion',
      '3': 'acciones',
    }
    object_list = self.model.objects.all()
    search_text = request.GET.get('sSearch', '').lower()
    start = int(request.GET.get('iDisplayStart', 0))
    delta = int(request.GET.get('iDisplayLength', 50))
    sort_dir = request.GET.get('sSortDir_0', 'asc')
    sort_col = int(request.GET.get('iSortCol_0', 0))
    sort_col_name = request.GET.get('mDataProp_%s' % sort_col, '1')
    sort_dir_prefix = (sort_dir == 'desc' and '-' or '')

    if sort_col_name in col_name_map:
      sort_col = col_name_map[sort_col_name]
      object_list = object_list.order_by('%s%s' % (sort_dir_prefix, sort_col))

    filtered_object_list = object_list
    if len(search_text) > 0:
      filtered_object_list = object_list.filter_on_search(search_text)

    json = {
      "iTotalRecords": object_list.count(),
      "iTotalDisplayRecords": filtered_object_list.count(),
      "sEcho": request.GET.get('sEcho', 1),
      "aaData": [obj.as_list() for obj in filtered_object_list[start:(start+delta)]]
    }
    return self.render_json_response(json)

class MedicamentoAutocomplete(View):
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
  def get(self, *args, **kwargs):
      q = self.request.GET['q']
      qs = Medicamento.objects.filter(Q(nombre__icontains=q))
      qs = self.get_results(qs)        
      return JsonResponse({
          'results': qs
      }, content_type='application/json')

  def get_results(self, results):
      return [dict(id=x.id, text=x.nombre, indicacion=x.indicacion, presentacion=self.PRESENTACION_PRINT[x.presentacion] ) for x in results]

class AjaxListView(ListView):
  template_name = 'medicamento/ajax/lista.html'
  model = Medicamento
  context_object_name = 'medicamentos'

class AjaxCrearView(CreateView):
  model = Medicamento
  form_class = MedicamentoForm
  template_name = 'medicamento/ajax/crear.html'

  def form_valid(self, form):
    model = form.save(commit=False)
    model.save()
    return render(self.request, 'paciente/success.html')
        
class AjaxEditarView(UpdateView):
  template_name = 'medicamento/ajax/editar.html'
  model = Medicamento
  form_class = MedicamentoForm
  context_object_name = "medicamento"

  def form_valid(self, form):
    model = form.save(commit=False)
    model.save()
    return render(self.request, 'paciente/success.html')

class AjaxEliminarView(View):
  def get(self, request):
    data = {
      'id': request.GET.get('id')
    }
    tipo_lente = Medicamento.objects.get(pk=request.GET.get('id'))
    tipo_lente.delete()
    return JsonResponse(data)