from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from .models import Seguro
from .forms import SeguroForm
# Create your views here.

class IndexView(ListView):
  template_name = 'seguro/index.html'
  model = Seguro
  context_object_name = 'seguros'

class SeguroRegistrar(CreateView):
  model = Seguro
  form_class = SeguroForm
  template_name = 'seguro/registrar.html'

  def form_valid(self, form):
    self.object = form.save()
    return render(self.request, 'paciente/success.html')