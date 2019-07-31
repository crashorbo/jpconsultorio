from django.shortcuts import render
from django.views.generic import ListView, View, UpdateView, CreateView, TemplateView
from braces.views import JSONResponseMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render

from .models import Tipolente
from .forms import TipolenteForm

# Create your views here.
class IndexView(TemplateView):
    template_name = 'configuracion/index.html'

class TableAsJSON(JSONResponseMixin, View):
  model = Tipolente

  def get(self, request, *args, **kwargs):
    col_name_map = {
      '0': 'nombre',
      '1': 'direccion',
      '2': 'telefono',
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

class AjaxListView(ListView):
  template_name = 'configuracion/ajax/tipolente/lista.html'
  model = Tipolente
  context_object_name = 'servicios'

class AjaxCrearView(CreateView):
  model = Tipolente
  form_class = TipolenteForm
  template_name = 'configuracion/ajax/tipolente/crear.html'

  def form_valid(self, form):
    self.object = form.save()
    return JsonResponse({"success": True})
  
  def form_invalid(self, form):
    return JsonResponse({"success": False, "errores": [(k, v[0]) for k, v in form.errors.items()]})
        
class AjaxEditarView(UpdateView):
  template_name = 'configuracion/ajax/tipolente/editar.html'
  model = Tipolente
  form_class = TipolenteForm
  context_object_name = "servicio"

  def form_valid(self, form):
    self.object = form.save()
    return JsonResponse({"success": True})
  
  def form_invalid(self, form):
    return JsonResponse({"success": False, "errores": [(k, v[0]) for k, v in form.errors.items()]})

class AjaxEliminarView(View):
  def get(self, request):
    data = {
      'id': request.GET.get('id')
    }
    tipo_lente = Tipolente.objects.get(pk=request.GET.get('id'))
    tipo_lente.delete()
    return JsonResponse(data)