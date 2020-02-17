from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, FormView
from agenda.models import Agenda, Agendaserv
from .models import Reportegeneral
from .forms import ReportegeneralForm

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
        particular = Agendaserv.objects.filter(agenda__fecha__year=self.object.gestion, agenda__fecha__month=self.object.mes, agenda__tipo=0)
        seguro = Agendaserv.objects.filter(agenda__fecha__year=self.object.gestion, agenda__fecha__month=self.object.mes, agenda__tipo=1)
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


class SeguroView(ListView):
    template_name = 'reporte/ajax/seguro.html'
    model = Agenda
