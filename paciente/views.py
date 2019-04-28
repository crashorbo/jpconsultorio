from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.http import JsonResponse
# Create your views here.
from .models import Paciente
from .forms import PacienteForm

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

  def form_valid(self, form):
    self.object = form.save()
    return render(self.request, 'paciente/success.html')