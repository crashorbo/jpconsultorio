import json
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View, CreateView, ListView, UpdateView, DeleteView
from dal import autocomplete
from django.db.models import Q
from datetime import datetime, timedelta
from django.urls import reverse
from django.db import transaction
from datetime import date, datetime
from django.utils.dateparse import parse_date
# Create your views here.
from paciente.models import Paciente
from core.models import Movdiario
from .models import Agenda, Diagnostico, Tratamiento, Agendaserv
from .forms import AgendaForm, DiagnosticoForm, TratamientoForm, ServicioFormset
# Vista Inicial de la aplicacion
class IndexView(CreateView):
    template_name = 'agenda/index.html'
    form_class = AgendaForm

    def get_context_data(self, **kwargs):
        data = super(IndexView, self).get_context_data(**kwargs)
        data['agendaserv'] = ServicioFormset(prefix='agendaserv')
        return data

class PacienteAutocomplete(View):
    def get(self, *args, **kwargs):
        q = self.request.GET['q']
        qs = Paciente.objects.filter(Q(nombres__icontains=q) | Q(apellidos__icontains=q) | Q(nro_documento__istartswith=q))
        qs = self.get_results(qs)        
        return JsonResponse({
            'results': qs
        }, content_type='application/json')

    def get_results(self, results):
        return [dict(id=x.id, text=x.nombres+' '+x.apellidos+' - '+x.nro_documento) for x in results]

class AgendaRegistrar(CreateView):
    model = Agenda
    form_class = AgendaForm
    template_name = 'paciente/registrar.html'
  
    def get_context_data(self, **kwargs):
        data = super(AgendaRegistrar, self).get_context_data(**kwargs)
        if self.request.POST:
            data['servicios'] = ServicioFormset(self.request.POST, prefix='agendaserv')
        else:
            data['servicios'] = ServicioFormset(prefix='agendaserv')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        servicios = context['servicios']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.hora_fin = (datetime.combine(datetime.today(), self.object.hora_inicio)+timedelta(minutes=30)).time()
            if self.object.tipo == 0:
                self.object.procedencia = 'PARTICULAR'
            elif self.object.tipo == 1:
                self.object.procedencia = self.object.seguro.nombre
            self.object.save()
            if servicios.is_valid():
                servicios.instance = self.object
                servicios.save()
            self.recalculo()
        return render(self.request, 'paciente/success.html')
    
    def recalculo(self):
        hoy = datetime.now()
        try:
            movdiario = Movdiario.objects.get(fecha=date(hoy.year,hoy.month,hoy.day),estado=True)
        except Movdiario.DoesNotExist:
            print(date(hoy.year,hoy.month,hoy.day))
            movdiario = Movdiario(parse_date(date(hoy.year,hoy.month,hoy.day)), 0, 0, True)
            movdiario.save()
        return movdiario

class AgendaAjaxLista(View):
    def get(self, *args, **kwargs):
        qs = Agenda.objects.filter(estado__exact=0)
        qs = self.get_results(qs)
        return HttpResponse({
            json.dumps(qs)
        }, content_type='application/json')

    def get_results(self, results):
        TIPO_CHOICE = {
            0: 'bg-info',
            1: 'bg-purple',
        }
        return [dict(id=x.id,title=x.paciente.nombres+' '+x.paciente.apellidos, start=x.fecha.strftime("%Y-%m-%d" )+' '+x.hora_inicio.strftime("%H:%M:%S"), end=x.fecha.strftime("%Y-%m-%d" )+' '+x.hora_fin.strftime("%H:%M:%S"), className=TIPO_CHOICE[x.tipo]) for x in results]

class AgendaListar(ListView):
    template_name = 'agenda/listar.html'
    model = Agenda

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consultas'] = self.model.objects.filter(fecha__exact=datetime.now(), estado__exact=0)
        return context

class AgendaAjaxEspera(ListView):
    template_name = 'agenda/ajax/listar.html'
    model = Agenda

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consultas'] = self.model.objects.filter(fecha__exact=datetime.now(), estado__exact=0)
        return context

class AgendaAjaxEditar(UpdateView):
    model = Agenda
    form_class = AgendaForm
    template_name = 'agenda/editarajax.html'
    context_object_name = 'agenda'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.hora_fin = (datetime.combine(datetime.today(), model.hora_inicio)+timedelta(minutes=30)).time()
        model.save()
        return render(self.request, 'paciente/success.html')

class AgendaAjaxDelete(DeleteView):
    model = Agenda
    template_name = 'agenda/eliminar.html'
    context_object_name = 'agenda'

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return render(self.request, 'paciente/success.html')

class AgendaEditar(UpdateView):
    model = Agenda
    form_class = AgendaForm
    template_name = 'agenda/editar.html'
    context_object_name = 'consulta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        diag_data = {'agenda': self.kwargs['pk']}
        diagnostico = DiagnosticoForm(initial=diag_data)
        tratamiento = TratamientoForm(initial=diag_data)
        context['diagform'] = diagnostico
        context['tratform'] = tratamiento
        return context

    def form_valid(self, form):
        model = form.save(commit=False)
        model.estado = 1
        model.save()
        return render(self.request, 'paciente/success.html')

class HistoriaListar(ListView):
    template_name = 'agenda/ajax/historia.html'
    model = Agenda

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historias'] = self.model.objects.filter(paciente__exact=self.kwargs['pk'], estado__exact=1)
        return context


class DiagnosticoCrear(CreateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'paciente/success.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        consulta = Agenda.objects.get(pk=model.agenda.id)
        model.save()
        return render(self.request, 'agenda/ajax/diagnosticos.html', context={'consulta': consulta })

class DiagnosticoEliminar(DeleteView):
    model = Diagnostico
    context_object_name = 'diagnostico'

    def delete(self, request, *args, **kwargs):
        model = self.get_object()
        consulta = Agenda.objects.get(pk=model.agenda.id)
        model.delete()
        return render(self.request, 'agenda/ajax/diagnosticos.html', context={'consulta': consulta })

class TratamientoCrear(CreateView):
    model = Tratamiento
    form_class = TratamientoForm
    template_name = 'paciente/success.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        consulta = Agenda.objects.get(pk=model.agenda.id)
        model.save()
        return render(self.request, 'agenda/ajax/tratamientos.html', context={'consulta': consulta })

class TratamientoEliminar(DeleteView):
    model = Tratamiento
    context_object_name = 'diagnostico'

    def delete(self, request, *args, **kwargs):
        model = self.get_object()
        consulta = Agenda.objects.get(pk=model.agenda.id)
        model.delete()
        return render(self.request, 'agenda/ajax/tratamientos.html', context={'consulta': consulta })

class DiagnosticoListar(ListView):
    template_name = 'agenda/diaglistar.html'
    
    def get_queryset(self, *args, **kwargs):
        self.agenda = get_object_or_404(Agenda, pk=self.kwargs['pk'])
        return Diagnostico.objects.filter(agenda=self.agenda)