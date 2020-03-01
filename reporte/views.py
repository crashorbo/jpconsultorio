from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, FormView, View
from agenda.models import Agenda, Agendaserv, Seguro
from .models import Reportegeneral, Reporteseguro
from .forms import ReportegeneralForm, ReporteseguroForm
from .utils import ReportePdfSeguro
import datetime


class IndexView(TemplateView):
    template_name = 'reporte/index.html'


class GeneralView(TemplateView):
    template_name = 'reporte/ajax/general.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.date.today().year
        frango = list(range(now, 2007, -1))
        context['rangestion'] = frango
        return context


class GeneralajaxView(TemplateView):
    template_name = 'reporte/ajax/general-ajax.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        general = Reportegeneral.objects.filter(gestion=self.kwargs['pk'])
        context['general'] = general
        return context


class GeneralformView(FormView):
    template_name = 'reporte/ajax/general-form.html'
    form_class = ReportegeneralForm
    success_url = '/thanks/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gestion = self.kwargs['pk']
        context['gestion'] = gestion
        form = ReportegeneralForm(initial={'gestion': self.kwargs['pk']})
        context['form'] = form
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            reporte_general = Reportegeneral.objects.get(gestion=self.object.gestion, mes=self.object.mes)
        except:
            particular = Agendaserv.objects.filter(fecha__year=self.object.gestion, fecha__month=self.object.mes, agenda__tipo=0,
                                                   agenda__deleted=False)
            seguro = Agendaserv.objects.filter(fecha__year=self.object.gestion, fecha__month=self.object.mes,
                                               agenda__tipo=1, agenda__deleted=False)
            suma_particular = 0
            suma_seguro = 0
            for item in particular:
                suma_particular = suma_particular + item.costo
            for item in seguro:
                suma_seguro = suma_seguro + item.costo
            self.object.particular = suma_particular
            self.object.seguro = suma_seguro
            self.object.save()
        return JsonResponse({"success": True})


class SeguroView(TemplateView):
    template_name = 'reporte/ajax/seguro.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.date.today().year
        frango = list(range(now, 2007, -1))
        seguros = Seguro.objects.all()
        context['rangestion'] = frango
        context['seguros'] = seguros
        return context

class SeguroajaxView(TemplateView):
    template_name = 'reporte/ajax/seguro-ajax.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        seguro = Reporteseguro.objects.filter(gestion=self.kwargs['gestion'], seguro=self.kwargs['pk'])
        context['seguro'] = seguro
        return context

class SeguroformView(FormView):
    template_name = 'reporte/ajax/seguro-form.html'
    form_class = ReporteseguroForm
    success_url = '/thanks/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gestion = self.kwargs['gestion']
        context['gestion'] = gestion
        seguro = self.kwargs['pk']
        context['seguro'] = seguro
        form = ReporteseguroForm(initial={'seguro': self.kwargs['pk'], 'gestion': self.kwargs['gestion']})
        context['form'] = form
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            seguro_reporte = Reporteseguro.objects.get(gestion=self.object.gestion, mes=self.object.mes, seguro=self.object.seguro)
        except:
            seguro = Agendaserv.objects.filter(fecha__year=self.object.gestion, fecha__month=self.object.mes, agenda__tipo=1,\
                                               agenda__seguro=self.object.seguro, agenda__deleted=False)
            suma_seguro = 0
            for item in seguro:
                suma_seguro = suma_seguro + item.costo
            self.object.monto = suma_seguro
            self.object.save()
        return JsonResponse({"success": True})

class SeguroPdfView(View):
    def get(self, *args, **kwargs):
        reporte_seguro = ReportePdfSeguro(id_reporte_seguro=self.kwargs['pk'])
        return reporte_seguro.generar_reporte()