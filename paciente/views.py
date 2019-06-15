from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import View
from django.http import JsonResponse
# Create your views here.
from braces.views import JSONResponseMixin
from .models import Paciente
from .forms import PacienteForm

class TableAsJSON(JSONResponseMixin, View):
  model = Paciente

  def get(self, request, *args, **kwargs):
    col_name_map = {
      '0': 'nombres',
      '1': 'documento',
      '2': 'nro_documento',
      '3': 'telefono',
      '4': 'codigo',
      '5': 'acciones',
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

# Vista Inicial de la aplicacion
class IndexView(ListView):
  template_name = 'paciente/index.html'
  model = Paciente
  form_class = PacienteForm

  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = self.model.objects.all()
        return context

class PacienteRegistrar(CreateView):
  model = Paciente
  form_class = PacienteForm
  template_name = 'paciente/registrar.html'

  def form_valid(self, form):
    self.object = form.save()
    return render(self.request, 'paciente/success.html')

class PacienteEditar(UpdateView):
  model = Paciente
  form_class = PacienteForm
  template_name = 'paciente/editar.html'
  context_object_name = 'paciente'

  def form_valid(self, form):
    self.object = form.save()
    return render(self.request, 'paciente/success.html')

class PacienteEliminar(View):
  def get(self, request):
    data = {
      'id': request.GET.get('id')
    }
    paciente = Paciente.objects.get(pk=request.GET.get('id'))
    paciente.delete()
    return JsonResponse(data)