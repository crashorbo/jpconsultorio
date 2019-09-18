import json
import locale
import os
from django.conf import settings
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, CreateView, ListView, UpdateView, DeleteView, DetailView
from dal import autocomplete
from django.db.models import Q
from datetime import datetime, timedelta
from django.urls import reverse
from django.db import transaction
from datetime import date, datetime
from django.utils.dateparse import parse_date
# Create your views here.
from paciente.models import Paciente
from paciente.templatetags import paciente_tags
from configuracion.models import Tipolente
from core.models import Movdiario
from paciente.forms import PacienteForm
from .models import Agenda, Diagnostico, Tratamiento, Agendaserv, Receta, Reconsulta, Agendaserv
from .forms import AgendaForm, DiagnosticoForm, TratamientoForm, ServicioFormset, RecetaForm, ReconsultaForm, AgendaservicioForm
from io import BytesIO
from decimal import Decimal, getcontext
from django.utils import formats
import textwrap

from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, BaseDocTemplate, PageTemplate, NextPageTemplate, PageBreak, Frame, FrameBreak, Flowable, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, inch
from reportlab.graphics.shapes import Drawing 
from reportlab.graphics.barcode.qr import QrCodeWidget 
from reportlab.graphics import renderPDF
from reportlab.lib.utils import ImageReader
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
        object_list = Paciente.objects.all()
        filtered_object_list = object_list
        if len(q) > 0:
            filtered_object_list = object_list.filter_on_search(q)
        qs = filtered_object_list
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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.hora_fin = (datetime.combine(datetime.today(), self.object.hora_inicio)+timedelta(minutes=15)).time()
        if self.object.tipo == 0:
            self.object.procedencia = 'PARTICULAR'
        elif self.object.tipo == 1:
            self.object.procedencia = self.object.seguro.nombre
        self.object.save()
        self.recalculo()
        return render(self.request, 'paciente/success.html')

    def recalculo(self):
        hoy = datetime.now()
        fecha = hoy.strftime("%Y-%m-%d")
        try:
            movimiento = Movdiario.objects.get(fecha=datetime.strptime(fecha, "%Y-%m-%d"))
        except Movdiario.DoesNotExist:
            movimiento = Movdiario(fecha=datetime.strptime(fecha, "%Y-%m-%d"), ingreso=0, egreso=0, estado=True)            
        servicios = Agendaserv.objects.filter(fecha=datetime.strptime(fecha, "%Y-%m-%d"))
        valor = 0
        for serv in servicios:
            if serv.estado:
                valor = valor + serv.costo
        movimiento.ingreso = valor
        movimiento.save()

class AgendaAjaxRegistrar(CreateView):
    model = Agenda
    form_class = AgendaForm
    template_name = 'agenda/ajax/registrar.html'

    def get_context_data(self, **kwargs):
        data = super(AgendaAjaxRegistrar, self).get_context_data(**kwargs)
        if self.request.POST:
            data['agendaserv'] = ServicioFormset(self.request.POST, prefix='agendaserv')
        else:
            data['agendaserv'] = ServicioFormset(prefix='agendaserv')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        servicios = context['agendaserv']    
        if servicios.is_valid():
            with transaction.atomic():
                self.object = form.save(commit=False)
                self.object.hora_fin = (datetime.combine(datetime.today(), self.object.hora_inicio)+timedelta(minutes=15)).time()
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
        fecha = hoy.strftime("%Y-%m-%d")
        try:
            movimiento = Movdiario.objects.get(fecha=datetime.strptime(fecha, "%Y-%m-%d"))
        except Movdiario.DoesNotExist:
            movimiento = Movdiario(fecha=datetime.strptime(fecha, "%Y-%m-%d"), ingreso=0, egreso=0, estado=True)            
        servicios = Agendaserv.objects.filter(fecha=datetime.strptime(fecha, "%Y-%m-%d"))
        valor = 0
        for serv in servicios:
            if serv.estado:
                valor = valor + serv.costo
        movimiento.ingreso = valor
        movimiento.save()

class AgendaAjaxLista(View):
    def get(self, *args, **kwargs):
        qs = Agenda.objects.filter(fecha__range=(self.request.GET['start'], self.request.GET['end']), deleted=False)
        qs = self.get_results(qs)
        return HttpResponse({
            json.dumps(qs)
        }, content_type='application/json')

    def get_results(self, results):
        TIPO_CHOICE = {
            0: 'bg-warning',
            1: 'bg-success',
            2: 'bg-danger'
        }
        return [dict(id=x.id,title=x.paciente.nombres+' '+x.paciente.apellidos, start=x.fecha.strftime("%Y-%m-%d" )+' '+x.hora_inicio.strftime("%H:%M:%S"), end=x.fecha.strftime("%Y-%m-%d" )+' '+x.hora_fin.strftime("%H:%M:%S"), className=TIPO_CHOICE[self.calculo(x)]) for x in results]

    def calculo(self, objeto):
        fecha = date.today()
        valor = 0
        if objeto.estado:
            valor = 2
        else:
            for item in objeto.agendaserv_set.all():
                if item.fecha == fecha:
                    valor = 1
                    break
        return valor

class AgendaListar(ListView):
    template_name = 'agenda/listar.html'
    model = Agenda

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consultas'] = self.model.objects.filter(fecha__exact=datetime.now(), deleted=False)
        return context

class AgendaFechaListar(View):
    def get(self, *args, **kwargs):
        q = self.request.GET['fecha']
        fecha = datetime.strptime(q, "%d-%m-%Y")
        qs = Agenda.objects.filter(fecha=fecha, deleted=False)
        fecha_aux = date.today()
        final = []
        for item in qs:
            if item.estado:
                final.append(item)
            else:
                for x in item.agendaserv_set.all():
                    if x.fecha == fecha_aux:
                        final.append(item)
                        break

        return render(self.request, 'agenda/ajax/listaconsultas.html', {'consultas': final})

class AgendaAjaxEspera(ListView):
    template_name = 'agenda/ajax/listar.html'
    model = Agenda

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.model.objects.filter(fecha__exact=datetime.now(), deleted=False).order_by('hora_inicio')
        fecha = date.today()
        final = []
        for item in qs:
            for x in item.agendaserv_set.all():
                if x.fecha == fecha:
                    final.append(item)
                    break
        context['consultas'] = final
        return context

class AgendaAjaxEditar(UpdateView):
    model = Agenda
    form_class = AgendaForm
    template_name = 'agenda/editarajax.html'
    context_object_name = 'agenda'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {'agenda': self.kwargs['pk']}
        agenda = Agenda.objects.get(id=self.kwargs['pk'])
        paciente = Paciente.objects.get(id=agenda.paciente.id)
        pacienteForm = PacienteForm(instance=paciente)
        servicio = AgendaservicioForm(data)
        context['servicioform'] = servicio
        context['pacienteform'] = pacienteForm
        context['paciente'] = paciente
        return context

    def form_valid(self, form):
        model = form.save(commit=False)
        agenda = Agenda.objects.get(id=model.id)
        if not agenda.estado:
            model.hora_fin = (datetime.combine(datetime.today(), model.hora_inicio)+timedelta(minutes=15)).time()
        else:
            model.fecha = agenda.fecha
            model.hora_inicio = agenda.hora_inicio
        model.save()
        return JsonResponse({"success": True})
    
    def form_invalid(self, form):
        return JsonResponse({"success": False, "mensaje": "Ha ocurrido un error en el sistema: ", "errores": [(k, v[0]) for k, v in form.errors.items()]})

class AgendaServicioCrear(CreateView):
    model = Agendaserv
    form_class = AgendaservicioForm
    template_name = 'agenda/editarajax.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.save()
        agenda = Agenda.objects.get(id=model.agenda.id)
        self.recalculo()
        return render(self.request, 'agenda/ajax/servicios.html', {'agenda': agenda})

    def recalculo(self):
        hoy = datetime.now()
        fecha = hoy.strftime("%Y-%m-%d")
        try:
            movimiento = Movdiario.objects.get(fecha=datetime.strptime(fecha, "%Y-%m-%d"))
        except Movdiario.DoesNotExist:
            movimiento = Movdiario(fecha=datetime.strptime(fecha, "%Y-%m-%d"), ingreso=0, egreso=0, estado=True)
        servicios = Agendaserv.objects.filter(fecha=datetime.strptime(fecha, "%Y-%m-%d"))
        valor = 0
        for serv in servicios:
            if not serv.agenda.tipo:
                valor = valor + serv.costo
        movimiento.ingreso = valor
        movimiento.save()

class AgendaAjaxDelete(DeleteView):
    model = Agenda
    template_name = 'agenda/eliminar.html'
    context_object_name = 'agenda'

    def delete(self, request, *args, **kwargs):
        borrar = self.get_object()
        if (not borrar.estado) and (not borrar.control):
            borrar.deleted = True            
            borrar.save()
            for serv in borrar.agendaserv_set.all():
                serv.delete()
            self.recalculo()
        if borrar.control:
            borrar.estado = True
            borrar.control = False
            borrar.fecha = borrar.fecha_consulta
            borrar.save()
        return render(self.request, 'paciente/success.html')
    
    def recalculo(self):
        hoy = datetime.now()
        fecha = hoy.strftime("%Y-%m-%d")
        try:
            movimiento = Movdiario.objects.get(fecha=datetime.strptime(fecha, "%Y-%m-%d"))
        except Movdiario.DoesNotExist:
            movimiento = Movdiario(fecha=datetime.strptime(fecha, "%Y-%m-%d"), ingreso=0, egreso=0, estado=True)            
        servicios = Agendaserv.objects.filter(fecha=datetime.strptime(fecha, "%Y-%m-%d"))
        valor = 0
        for serv in servicios:
            if not serv.agenda.tipo:
                valor = valor + serv.costo
        movimiento.ingreso = valor
        movimiento.save()

class AgendaEditar(UpdateView):
    model = Agenda
    form_class = AgendaForm
    template_name = 'agenda/editar.html'
    context_object_name = 'consulta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agenda = Agenda.objects.get(id=self.kwargs['pk'])
        visor = Agenda.objects.filter(paciente=agenda.paciente).exclude(id=agenda.id).order_by('-fecha')
        diag_data = {'agenda': self.kwargs['pk']}
        descuento = False
        for item in agenda.agendaserv_set.all():
            if item.descuento:
                descuento = True
                break
        diagnostico = DiagnosticoForm(initial=diag_data)
        tratamiento = TratamientoForm(initial=diag_data)
        receta = RecetaForm(initial=diag_data)
        control = ReconsultaForm(initial=diag_data)
        tipolentes = Tipolente.objects.all()
        if len(visor) > 0:
            context['visor'] = visor[0]
        else:
            context['visor'] = None
        context['tipolentes'] = tipolentes
        context['diagform'] = diagnostico
        context['tratform'] = tratamiento
        context['recetaform'] = receta
        context['controlform'] = control
        context['descuento'] = descuento
        return context

    def form_valid(self, form):
        model = form.save(commit=False)
        agenda = Agenda.objects.get(id=model.id)
        print(agenda.fecha_consulta)
        if agenda.control:
            model.fecha_consulta = agenda.fecha_consulta
            model.fecha = datetime.today()
        print(model.fecha)
        model.estado = 1
        model.save()
        return JsonResponse({"success": True})

    def form_invalid(self, form):
        return JsonResponse({"success": False})

class HistoriaListar(ListView):
    template_name = 'agenda/ajax/historia.html'
    model = Agenda

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        historias = self.model.objects.filter(paciente__exact=self.kwargs['pk'], estado__exact=1, deleted=False).order_by('-fecha')
        context['historias'] = historias
        if len(historias) > 0:
            context['historia'] = historias[0]
        else:
            context['historia'] = None
        return context

class HistoriamListar(ListView):
    template_name = 'agenda/ajax/historia.html'
    model = Agenda

    def get_context_data(self, **kwargs):
        persona, agenda = [self.kwargs[x] for x in ['pk', 'id']]
        context = super().get_context_data(**kwargs)
        agenda = Agenda.objects.get(id=agenda)
        historias = self.model.objects.filter(paciente__exact=persona, estado__exact=1, deleted=False).exclude(id=agenda.id).order_by('-fecha')
        context['historias'] = historias
        if len(historias) > 0:
            context['historia'] = historias[0]
        else:
            context['historia'] = None
        return context

class HistoriaVer(DetailView):
    model = Agenda
    template_name = 'agenda/ajax/historiaver.html'
    context_object_name = 'historia'

class DiagnosticoCrear(CreateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'paciente/success.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        consulta = Agenda.objects.get(pk=model.agenda.id)
        consulta.estado = True
        consulta.save()
        model.save()
        return render(self.request, 'agenda/ajax/diagnosticos.html', context={'consulta': consulta })

class DiagnosticoEliminar(DeleteView):
    model = Diagnostico
    context_object_name = 'diagnostico'

    def delete(self, request, *args, **kwargs):
        model = self.get_object()
        consulta = Agenda.objects.get(pk=model.agenda.id)
        consulta.estado = True
        consulta.save()
        model.delete()
        return render(self.request, 'agenda/ajax/diagnosticos.html', context={'consulta': consulta })

class TratamientoCrear(CreateView):
    model = Tratamiento
    form_class = TratamientoForm
    template_name = 'paciente/success.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        consulta = Agenda.objects.get(pk=model.agenda.id)
        consulta.estado = True
        consulta.save()
        model.save()
        return render(self.request, 'agenda/ajax/tratamientos.html', context={'consulta': consulta })

class TratamientoEliminar(DeleteView):
    model = Tratamiento
    context_object_name = 'diagnostico'

    def delete(self, request, *args, **kwargs):
        model = self.get_object()
        consulta = Agenda.objects.get(pk=model.agenda.id)
        consulta.estado = True
        consulta.save()
        model.delete()
        return render(self.request, 'agenda/ajax/tratamientos.html', context={ 'consulta': consulta })

class ReconsultaCrear(CreateView):
    model = Reconsulta
    form_class = ReconsultaForm
    template_name = 'paciente/success.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        consulta = Agenda.objects.get(pk=model.agenda.id)
        consulta.estado = True
        consulta.save()
        model.save()
        return render(self.request, 'agenda/ajax/controles.html', context={'consulta': consulta })

class ReconsultaEliminar(DeleteView):
    model = Reconsulta
    context_object_name = 'diagnostico'

    def delete(self, request, *args, **kwargs):
        model = self.get_object()
        consulta = Agenda.objects.get(pk=model.agenda.id)
        consulta.estado = True
        consulta.save()
        model.delete()
        return render(self.request, 'agenda/ajax/controles.html', context={ 'consulta': consulta })

class RecetaCrear(CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'paciente/success.html'

    def form_valid(self, form):
        model = form.save(commit=False)
        consulta = Agenda.objects.get(pk=model.agenda.id)
        model.save()
        return render(self.request, 'agenda/ajax/recetas.html', context={'consulta': consulta })

class RecetaEliminar(DeleteView):
    model = Receta
    context_object_name = 'receta'

    def delete(self, request, *args, **kwargs):
        model = self.get_object()
        consulta = Agenda.objects.get(pk=model.agenda.id)
        model.delete()
        return render(self.request, 'agenda/ajax/recetas.html', context={ 'consulta': consulta })

class DiagnosticoListar(ListView):
    template_name = 'agenda/diaglistar.html'
    
    def get_queryset(self, *args, **kwargs):
        self.agenda = get_object_or_404(Agenda, pk=self.kwargs['pk'])
        return Diagnostico.objects.filter(agenda=self.agenda)
class AgendaservUpdate(View):
    def get(self, *args, **kwargs):
        servicio = Agendaserv.objects.get(id=self.kwargs['pk'])
        servicio.estado = True
        servicio.fecha = datetime.now()
        servicio.save()
        agenda = Agenda.objects.get(id=servicio.agenda.id)
        self.recalculo()
        return render(self.request, 'agenda/ajax/listacobrar.html', context={ 'agenda': agenda })

    def recalculo(self):
        hoy = datetime.now()
        fecha = hoy.strftime("%Y-%m-%d")
        try:
            movimiento = Movdiario.objects.get(fecha=datetime.strptime(fecha, "%Y-%m-%d"))
        except Movdiario.DoesNotExist:
            movimiento = Movdiario(fecha=datetime.strptime(fecha, "%Y-%m-%d"), ingreso=0, egreso=0, estado=True)            
        servicios = Agendaserv.objects.filter(fecha=datetime.strptime(fecha, "%Y-%m-%d"))
        valor = 0
        for serv in servicios:
            if serv.estado:
                valor = valor + serv.costo
        movimiento.ingreso = valor
        movimiento.save()

class ControlView(CreateView):
    model = Agenda
    form_class = AgendaForm
    template_name = 'paciente/registrar.html'
    
    def form_valid(self, form):
        model = form.save(commit=False)
        agendas = Agenda.objects.filter(paciente=model.paciente, deleted=False).order_by('-fecha')
        if agendas:
            agenda = agendas[0]
            if agenda.estado:
                agenda.hora_inicio = model.hora_inicio
                agenda.hora_fin = (datetime.combine(datetime.today(), model.hora_inicio)+timedelta(minutes=15)).time()
                agenda.fecha = model.fecha
                agenda.estado = False
                agenda.control = True
                agenda.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "mensaje": "Ya se ha registrado el control para "+agenda.paciente.nombres+" "+agenda.paciente.apellidos})
        else:
            return JsonResponse({"success": False, "mensaje": model.paciente.nombres+" "+model.paciente.apellidos+" no tiene un Historial"})

    def form_invalid(self, form):
        return JsonResponse({"success": False, "mensaje": "Ha ocurrido un error con el envio de datos, revise si selecciono un Paciente"})

class Reportemov(View):
    def get(self, *args, **kwargs):
        hoy = datetime.now()
        fecha = hoy.strftime("%Y%m%d")
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "mov_"+fecha+".pdf"  # llamado clientes
        # la linea 26 es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=portrait(letter),
                                rightMargin=30,
                                leftMargin=30,
                                topMargin=30,
                                bottomMargin=30,
                                )

        cabeza = ParagraphStyle(name="cabeza", alignment=TA_LEFT, fontSize=14, fontName="Times-Roman", textColor=colors.darkblue)
        cabecera = ParagraphStyle(name="cabecera", alignment=TA_CENTER, fontSize=10, fontName="Times-Roman", textColor=colors.white)
        celdaderecha = ParagraphStyle(name="celdaderecha",alignment=TA_RIGHT, fontsize=8, fontName="Times-Roman")
        celdaderechabold = ParagraphStyle(name="celdaderecha",alignment=TA_RIGHT, fontsize=10, fontName="Times-Bold")
        celda = ParagraphStyle(name="celda", alignment=TA_LEFT, fontsize=8, fontName="Times-Roman")
        celdabold = ParagraphStyle(name="celda", alignment=TA_LEFT, fontsize=10, fontName="Times-Bold")
        celdaverde = ParagraphStyle(name="celdaverde", alignment=TA_CENTER, fontSize=8, fontName="Times-Roman", textColor=colors.green)
        celdaroja = ParagraphStyle(name="celdaroja", alignment=TA_CENTER, fontSize=8, fontName="Times-Roman", textColor=colors.red)
        celdarojarem = ParagraphStyle(name="celdaroja", alignment=TA_CENTER, fontSize=8, fontName="Times-Roman", textColor=colors.red, backColor = colors.yellow)
        celdaremarcada = ParagraphStyle(name="celda", alignment=TA_LEFT, fontsize=8, fontName="Times-Roman", backColor=colors.yellow)
        celdaremarcadader = ParagraphStyle(name="celdader", alignment=TA_RIGHT, fontsize=8, fontName="Times-Roman",
                                           backColor=colors.yellow)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER, fontSize=16))
        styles.add(ParagraphStyle(name='subtitulo', alignment=TA_LEFT, fontSize=14))
        header = Paragraph("Reporte Movimientos "+hoy.strftime("%d/%m/%Y"), styles['centered'])
        subparticular = Paragraph("Particulares:", styles['Heading2'])
        subasegurados = Paragraph("Asegurados:", styles['Heading2'])
        movimiento = []
        particulares = []
        asegurados = []
        total_particular_costo = 0
        total_particular_cobrado = 0
        total_asegurado_costo = 0
        movimiento.append(header)
        movimiento.append(subparticular)
        
        items = Agendaserv.objects.filter(fecha=datetime.strptime(hoy.strftime("%Y-%m-%d"), "%Y-%m-%d"), agenda__deleted=False)
        for item in items:
            if not item.agenda.tipo:
                if item.estado:
                    aux = item.costo
                    total_particular_cobrado = total_particular_cobrado + item.costo
                else:
                    aux = Decimal('0.00')
                if item.descuento:
                    this_particular = [
                        Paragraph((item.agenda.paciente.nombres + ' ' + item.agenda.paciente.apellidos), celdaremarcada),
                        Paragraph(item.servicio.nombre, celdaremarcada), Paragraph(str(item.costo), celdaremarcadader),
                    ]
                else:
                    this_particular = [
                        Paragraph((item.agenda.paciente.nombres + ' ' + item.agenda.paciente.apellidos), celda),
                        Paragraph(item.servicio.nombre, celda), Paragraph(str(item.costo), celdaderecha),
                    ]
                particulares.append(this_particular)
                total_particular_costo = total_particular_costo + item.costo
            else:
                if item.descuento:
                    this_asegurado = [
                        Paragraph((item.agenda.paciente.nombres+' '+item.agenda.paciente.apellidos), celdaremarcada),
                        Paragraph(item.servicio.nombre, celdaremarcada), Paragraph(str(item.agenda.procedencia), celdaremarcada),
                        Paragraph(str(item.costo), celdaremarcadader)
                    ]
                else:
                    this_asegurado = [
                        Paragraph((item.agenda.paciente.nombres + ' ' + item.agenda.paciente.apellidos), celda),
                        Paragraph(item.servicio.nombre, celda), Paragraph(str(item.agenda.procedencia), celda),
                        Paragraph(str(item.costo), celdaderecha)
                    ]
                asegurados.append(this_asegurado)
                total_asegurado_costo = total_asegurado_costo + item.costo
        this_particular = [Paragraph('TOTAL', celdabold), Paragraph('', celda), Paragraph(str(total_particular_costo), celdaderechabold)]
        particulares.append(this_particular)
        this_asegurado = [Paragraph('TOTAL', celdabold), Paragraph('', celda), Paragraph('', celda), Paragraph(str(total_asegurado_costo),celdaderechabold)]
        asegurados.append(this_asegurado)
        headings = (Paragraph('Nombre', cabecera), Paragraph('Consulta', cabecera), Paragraph('Costo', cabecera))
        t1 = Table([headings] + particulares, colWidths=[11 * cm, 6 * cm, 2 * cm])
        t1.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.black)
        ]
        ))

        headings = (Paragraph('Nombre', cabecera), Paragraph('Consulta', cabecera), Paragraph('Procedencia', cabecera), Paragraph('Costo',cabecera))
        t2 = Table([headings] + asegurados, colWidths=[8 * cm, 3 * cm, 6 * cm, 2 * cm])
        t2.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.black)
        ]
        ))


        movimiento.append(t1)
        movimiento.append(subasegurados)
        movimiento.append(t2)
        doc.build(movimiento)
        response.write(buff.getvalue())
        buff.close()
        return response

class Reportemovfecha(View):
    def get(self, *args, **kwargs):
        fecha = self.kwargs['date']
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "mov_"+fecha+".pdf"
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=portrait(letter),
                                rightMargin=30,
                                leftMargin=30,
                                topMargin=30,
                                bottomMargin=30,
                                )

        cabeza = ParagraphStyle(name="cabeza", alignment=TA_LEFT, fontSize=14, fontName="Times-Roman", textColor=colors.darkblue)
        cabecera = ParagraphStyle(name="cabecera", alignment=TA_CENTER, fontSize=10, fontName="Times-Roman", textColor=colors.white)
        celdaderecha = ParagraphStyle(name="celdaderecha",alignment=TA_RIGHT, fontsize=8, fontName="Times-Roman")
        celdaderechabold = ParagraphStyle(name="celdaderecha",alignment=TA_RIGHT, fontsize=10, fontName="Times-Bold")
        celda = ParagraphStyle(name="celda", alignment=TA_LEFT, fontsize=8, fontName="Times-Roman")
        celdabold = ParagraphStyle(name="celda", alignment=TA_LEFT, fontsize=10, fontName="Times-Bold")
        celdaverde = ParagraphStyle(name="celdaverde", alignment=TA_CENTER, fontSize=8, fontName="Times-Roman", textColor=colors.green)
        celdaroja = ParagraphStyle(name="celdaroja", alignment=TA_CENTER, fontSize=8, fontName="Times-Roman", textColor=colors.red)
        celdarojarem = ParagraphStyle(name="celdaroja", alignment=TA_CENTER, fontSize=8, fontName="Times-Roman", textColor=colors.red, backColor = colors.yellow)
        celdaremarcada = ParagraphStyle(name="celda", alignment=TA_LEFT, fontsize=8, fontName="Times-Roman", backColor = colors.yellow)
        celdaremarcadader = ParagraphStyle(name="celdader", alignment=TA_RIGHT, fontsize=8, fontName="Times-Roman",
                                           backColor=colors.yellow)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER, fontSize=16))
        styles.add(ParagraphStyle(name='subtitulo', alignment=TA_LEFT, fontSize=14))
        header = Paragraph("Reporte Movimientos "+fecha, styles['centered'])
        subparticular = Paragraph("Particulares:", styles['Heading2'])
        subasegurados = Paragraph("Asegurados:", styles['Heading2'])
        subcontroles = Paragraph("Controles:", styles['Heading2'])
        movimiento = []
        particulares = []
        asegurados = []
        controles = []
        total_particular_costo = 0
        total_particular_cobrado = 0
        total_asegurado_costo = 0
        movimiento.append(header)
        movimiento.append(subparticular)
        items = Agendaserv.objects.filter(fecha=datetime.strptime(fecha, "%d-%m-%Y"), agenda__deleted=False)
        for item in items:
            if not item.agenda.tipo:
                if item.estado:
                    aux = item.costo
                    total_particular_cobrado = total_particular_cobrado + item.costo
                else:
                    aux = Decimal('0.00')
                if item.descuento:
                    this_particular = [
                        Paragraph((item.agenda.paciente.nombres + ' ' + item.agenda.paciente.apellidos), celdaremarcada),
                        Paragraph(item.servicio.nombre, celdaremarcada), Paragraph(str(item.costo), celdaremarcadader),
                        Paragraph(str(aux), celdaremarcadader)
                    ]
                else:
                    this_particular = [
                        Paragraph((item.agenda.paciente.nombres + ' ' + item.agenda.paciente.apellidos), celda),
                        Paragraph(item.servicio.nombre, celda), Paragraph(str(item.costo), celdaderecha),
                        Paragraph(str(aux), celdaderecha)
                    ]
                particulares.append(this_particular)
                total_particular_costo = total_particular_costo + item.costo
            else:
                if item.descuento:
                    this_asegurado = [
                        Paragraph((item.agenda.paciente.nombres+' '+item.agenda.paciente.apellidos), celdaremarcada),
                        Paragraph(item.servicio.nombre, celdaremarcada), Paragraph(str(item.agenda.matricula), celdaremarcada),
                        Paragraph(item.agenda.tipo_beneficiario, celdaremarcada), Paragraph(str(item.costo), celdaremarcadader)
                    ]
                else:
                    this_asegurado = [
                        Paragraph((item.agenda.paciente.nombres + ' ' + item.agenda.paciente.apellidos), celda),
                        Paragraph(item.servicio.nombre, celda), Paragraph(str(item.agenda.matricula), celda),
                        Paragraph(item.agenda.tipo_beneficiario, celda), Paragraph(str(item.costo), celdaderecha)
                    ]
                asegurados.append(this_asegurado)
                total_asegurado_costo = total_asegurado_costo + item.costo
        this_particular = [Paragraph('TOTAL', celdabold), Paragraph('', celda), Paragraph(str(total_particular_costo), celdaderechabold), Paragraph(str(total_particular_cobrado),celdaderechabold)]
        particulares.append(this_particular)
        this_asegurado = [Paragraph('TOTAL', celdabold), Paragraph('', celda), Paragraph('', celda), Paragraph('', celda), Paragraph(str(total_asegurado_costo),celdaderechabold)]
        asegurados.append(this_asegurado)
        itemss = Agenda.objects.filter(fecha=datetime.strptime(fecha, "%d-%m-%Y"), control=True)
        for item in itemss:
            controles.append([Paragraph(item.paciente.nombres + ' ' + item.paciente.apellidos, celda), ])
        headings = (Paragraph('Nombre', cabecera), Paragraph('Consulta', cabecera), Paragraph('Costo', cabecera), Paragraph('SubTotal',cabecera))
        t1 = Table([headings] + particulares, colWidths=[10 * cm, 5 * cm, 2 * cm, 2 * cm])
        t1.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.black)
        ]
        ))

        headings = (Paragraph('Nombre', cabecera), Paragraph('Consulta', cabecera), Paragraph('matricula', cabecera), Paragraph('Procede', cabecera), Paragraph('Costo',cabecera))
        t2 = Table([headings] + asegurados, colWidths=[8 * cm, 4 * cm, 3 * cm, 2 * cm, 2 * cm])
        t2.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.black)
        ]
        ))

        headings = (Paragraph('Nombre', cabecera),)
        t3 = Table([headings] + controles, colWidths=[19 * cm, ])
        t3.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (6, -1), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.black)
            ]
        ))

        movimiento.append(t1)
        movimiento.append(subasegurados)
        movimiento.append(t2)
        movimiento.append(subcontroles)
        movimiento.append(t3)
        doc.build(movimiento)
        response.write(buff.getvalue())
        buff.close()
        return response
class Reporterec(View):
    def subrayar(self, pdf, x, y, texto):
        tam = len(texto)
        pdf.line(x-tam*4, y-4,x+tam*4,y-4)
    
    def subrayar2(self, pdf, x, y, texto):
        tam = len(texto)
        pdf.line(x, y-4,x+tam*8,y-4)

    def paciente(self, pdf):
        pdf.setFont("Times-Bold", 12)
        pdf.drawCentredString(210,430, self.agenda.paciente.nombres + ' ' + self.agenda.paciente.apellidos)
        self.subrayar(pdf, 210,430,self.agenda.paciente.nombres + ' ' +self.agenda.paciente.apellidos)

    def encabezado(self, pdf):
        pdf.setFont("Times-Bold", 12)
        pdf.drawCentredString(210,400, "RECETA DE LENTES")
        self.subrayar(pdf, 210,400, "RECETA DE LENTES")

    def subtitulo(self, pdf):
        pdf.setFont("Times-Bold", 12)
        if (self.agenda.adicion):
            pdf.drawString(55,370, "PARA LEJOS:")
            self.subrayar2(pdf, 55,370, "PARA LEJOS")
        else:
            pdf.drawString(55,370, "USO PERMANENTE:")
            self.subrayar2(pdf, 55,370, "USO PERMANENTE")

    def medida(self,pdf):
        if (self.agenda.impav):
            pdf.setFont("Times-Bold", 16)
            pdf.drawCentredString(75,305, "OD.")
            pdf.drawCentredString(75,275, "OI.")
            pdf.setFont("Times-Roman", 12)
            pdf.drawCentredString(130,335, "ESFERICO")
            pdf.drawCentredString(205,335, "CILINDRICO")
            pdf.drawCentredString(285,335, "EJE")
            pdf.drawCentredString(353,335, "A.V.")
            pdf.drawString(55, 255, "Favor Medir D.P.")
            pdf.setFont("Times-Roman", 16)
            if(self.agenda.drc1):
                pdf.drawCentredString(130,305, self.agenda.drc1)
            else:
                pdf.drawCentredString(130,305, '------')
            if(self.agenda.drc2):
                pdf.drawCentredString(205,305, self.agenda.drc2)
            else:
                pdf.drawCentredString(205,305, '------')
            if(self.agenda.irc1):
                pdf.drawCentredString(130,275, self.agenda.irc1)
            else:
                pdf.drawCentredString(130,275, '------')
            if(self.agenda.irc2):
                pdf.drawCentredString(205,275, self.agenda.irc2)
            else:
                pdf.drawCentredString(205,275, '------')
            pdf.setFont("Times-Bold", 16)
            if(self.agenda.drc3):
                pdf.drawCentredString(285,305, self.agenda.drc3+'°')
            else:
                pdf.drawCentredString(285,305, '------')
            if(self.agenda.irc3):
                pdf.drawCentredString(285,275, self.agenda.irc3+'°')
            else:
                pdf.drawCentredString(285,275, '------')
            pdf.setFont("Times-Roman", 16)
            if(self.agenda.dcc):
                pdf.drawCentredString(353,305, '20/'+self.agenda.dcc)
            else:
                pdf.drawCentredString(353,305, '------')
            if(self.agenda.irc3):
                pdf.drawCentredString(353,275, '20/'+self.agenda.icc)
            else:
                pdf.drawCentredString(353,275, '------')
        else:
            pdf.setFont("Times-Bold", 16)
            pdf.drawCentredString(90,305, "OD.")
            pdf.drawCentredString(90,275, "OI.")
            pdf.setFont("Times-Roman", 12)
            pdf.drawCentredString(150,335, "ESFERICO")
            pdf.drawCentredString(230,335, "CILINDRICO")
            pdf.drawCentredString(310,335, "EJE")
            pdf.drawString(70, 255, "Favor Medir D.P.")
            pdf.setFont("Times-Roman", 16)
            if(self.agenda.drc1):
                pdf.drawCentredString(150,305, self.agenda.drc1)
            else:
                pdf.drawCentredString(150,305, '------')
            if(self.agenda.drc2):
                pdf.drawCentredString(230,305, self.agenda.drc2)
            else:
                pdf.drawCentredString(230,305, '------')
            if(self.agenda.irc1):
                pdf.drawCentredString(150,275, self.agenda.irc1)
            else:
                pdf.drawCentredString(150,275, '------')
            if(self.agenda.irc2):
                pdf.drawCentredString(230,275, self.agenda.irc2)
            else:
                pdf.drawCentredString(230,275, '------')
            pdf.setFont("Times-Bold", 16)
            if(self.agenda.drc3):
                pdf.drawCentredString(310,305, self.agenda.drc3+'°')
            else:
                pdf.drawCentredString(310,305, self.agenda.drc3+'------')
            if(self.agenda.irc3):
                pdf.drawCentredString(310,275, self.agenda.irc3+'°')
            else:
                pdf.drawCentredString(310,275, '------')
        
    def observaciones(self, pdf, y):
        adicion = self.agenda.tipo_lente.split(",")
        pdf.setFont("Times-Bold", 12)
        pdf.drawString(70, y, "Obs.")
        pdf.setFont("Times-Roman", 10)
        pdf.setFillColorRGB(1,0,0)
        for item in adicion:
            pdf.drawString(130, y, item)
            y = y - 15
        y = y - 5
        pdf.setFillColorRGB(0,0,0)
        pdf.drawString(70, y, "No olvide traer sus lentes a control.")
        pdf.drawString(70, y-15, "No olvide traer su receta en la proxima consulta.")
        mes = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
        pdf.drawString(70, 55, str(date.today().day)+" - "+mes[date.today().month]+" - "+str(date.today().year))
        pdf.drawRightString(350, 55, datetime.now().strftime("(%H:%M:%S)"))

    def tabla(self, pdf):
        if (self.agenda.impav):
            pdf.line(55, 350 ,380, 350)
            pdf.line(55, 325 ,380, 325)
            pdf.line(55, 295 ,380, 295)
            pdf.line(55, 265 ,380, 265)
            pdf.line(55, 350 ,55, 265)
            pdf.line(95, 350 ,95, 265)
            pdf.line(165, 350 ,165, 265)
            pdf.line(245, 350 ,245, 265)
            pdf.line(325, 350 ,325, 265)
            pdf.line(380, 350 ,380, 265)
        else:
            pdf.line(70, 350 ,350, 350)
            pdf.line(70, 325 ,350, 325)
            pdf.line(70, 295 ,350, 295)
            pdf.line(70, 265 ,350, 265)
            pdf.line(70, 350 ,70, 265)
            pdf.line(110, 350 ,110, 265)
            pdf.line(190, 350 ,190, 265)
            pdf.line(270, 350 ,270, 265)
            pdf.line(350, 350 ,350, 265)

    def tablaa(self, pdf):
        if (self.agenda.impav):
            pdf.setFont("Times-Bold", 12)
            pdf.drawString(65,230, "PARA CERCA:")
            self.subrayar2(pdf, 65,230, "PARA CERCA")
            pdf.line(175, 240 ,335, 240)
            pdf.line(175, 210 ,335, 210)
            pdf.line(175, 240 ,175, 210)
            pdf.line(255, 240 , 255, 210)
            pdf.line(335, 240 , 335, 210)
            pdf.setFont("Times-Bold", 16)
            pdf.drawCentredString(215, 220,"ADICION")
            pdf.setFont("Times-Roman", 16)
            pdf.drawCentredString(295, 220, self.agenda.adicion)
        else:
            pdf.setFont("Times-Bold", 12)
            pdf.drawString(65,230, "PARA CERCA:")
            self.subrayar2(pdf, 65,230, "PARA CERCA")
            pdf.line(200, 240 ,360, 240)
            pdf.line(200, 210 ,360, 210)
            pdf.line(200, 240 ,200, 210)
            pdf.line(280, 240 , 280, 210)
            pdf.line(360, 240 , 360, 210)
            pdf.setFont("Times-Bold", 16)
            pdf.drawCentredString(240, 220,"ADICION")
            pdf.setFont("Times-Roman", 16)
            pdf.drawCentredString(320, 220, self.agenda.adicion)

    def get(self, *args, **kwargs):
        self.agenda = Agenda.objects.get(id=self.kwargs['pk'])
        recetam = (15*cm, 20*cm)
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "receta-lentes.pdf"  # llamado clientes
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer, pagesize=recetam)
        self.paciente(pdf)
        self.encabezado(pdf)
        self.subtitulo(pdf)
        self.medida(pdf)
        if (self.agenda.adicion):
            self.tablaa(pdf)
            self.observaciones(pdf, 190)
        else:
            self.observaciones(pdf, 230)
        self.tabla(pdf)
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
        
class ReporteRecmed(View):
    y = 390
    def subrayar(self, pdf, x, y, texto):
        tam = len(texto)
        pdf.line(x-tam*4, y-4,x+tam*4,y-4)
    
    def subrayar2(self, pdf, x, y, texto):
        tam = len(texto)
        pdf.line(x, y-4,x+tam*8,y-4)

    def paciente(self, pdf):
        pdf.setFont("Times-Bold", 12)
        pdf.drawCentredString(210,430, self.agenda.paciente.nombres + ' ' + self.agenda.paciente.apellidos)
        self.subrayar(pdf, 210,430,self.agenda.paciente.nombres + ' ' +self.agenda.paciente.apellidos)
        pdf.setFont("Times-Roman", 10)
        mes = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
        pdf.drawString(70, 55, str(date.today().day)+" - "+mes[date.today().month]+" - "+str(date.today().year))
        pdf.drawRightString(350, 55, datetime.now().strftime("(%H:%M:%S)"))

    def receta(self, pdf, numero, rec, factory):
        pdf.setFont("Times-Bold", 16)
        pdf.drawString(70, self.y, str(numero)+'.- '+rec.medicamento.nombre)
        pdf.setFont("Times-Bold", 12)
        pdf.setFillColorRGB(1,0,0)
        pdf.drawRightString(350, self.y, '('+rec.presentacion+')')
        self.y = self.y - factory
        pdf.drawRightString(350, self.y, '#'+str(rec.cantidad))
        pdf.setFillColorRGB(0,0,0)
        pdf.setFont("Times-Roman", 12)
        texto = textwrap.wrap(rec.indicacion, 50)
        self.y = self.y - factory
        pdf.setFont("Times-Bold", 12)
        pdf.drawString(90, self.y, ">")
        pdf.setFont("Times-Roman", 12)
        x = 0
        for item in texto:            
            pdf.drawString(105, self.y, texto[x])
            x = x+1
            self.y = self.y-15

    def get(self, *args, **kwargs):
        self.agenda = Agenda.objects.get(id=self.kwargs['pk'])
        recetam = (15*cm, 20*cm)
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "receta.pdf"  # llamado clientes
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer, pagesize=recetam)
        self.paciente(pdf)
        indice=1
        factory = 30
        x = self.agenda.receta_set.all().count()
        if x == 1:
            factory = 70
            self.y = self.y - 60        
        if x == 2:
            factory = 40
            self.y = self.y - 40        
        if x == 3:
            factory = 30
            self.y = self.y - 20 

        for item in self.agenda.receta_set.all():
            self.receta(pdf, indice, item, factory)
            self.y = self.y-factory-5
            indice = indice+1
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


class ReporteRecsegurob(View):
    def encabezado(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        #try:
        archivo_imagen1 = os.path.join(settings.MEDIA_ROOT, "imagenes","sistema","logo1.jpg")
        archivo_imagen2 = os.path.join(settings.MEDIA_ROOT, "imagenes","sistema","logo2.jpg") 
        #imagen = Image(pil_img, width=90, height=50, hAlign='LEFT')
        canvas.drawImage(archivo_imagen1, 75, 720,width=60, height=40)
        canvas.drawImage(archivo_imagen2, 150, 720,width=150, height=40)
        #except:
        #canvas.drawString(inch, letter[1] - 50, "Ejemplo de DocTemplate y PageTemplate")
        #canvas.line(inch, letter[1] - 60, letter[0] - 65, letter[1] - 60)
        canvas.restoreState()


    def cabecera(self, story, estilo, agenda):
        data = []
        story.append(NextPageTemplate('principal'))
        data.append((Paragraph("NOMBRE", estilo['Titulo']),Paragraph("EDAD",estilo['Titulo']),))
        data.append((Paragraph(agenda.paciente.nombres+" "+agenda.paciente.apellidos, estilo['Parrafo']),Paragraph(paciente_tags.edad(agenda.paciente.fecha_nacimiento), estilo['Parrafo']),))
        data.append((Paragraph("SEGURO", estilo['Titulo']), Paragraph("MATRICULA",estilo['Titulo']),))
        data.append((Paragraph(agenda.seguro.nombre, estilo['Parrafo']), Paragraph(agenda.matricula, estilo['Parrafo']),))
        data.append((Paragraph("FECHA", estilo['Titulo']), Paragraph("TIPO",estilo['Titulo']),))
        data.append((Paragraph(agenda.fecha.strftime("%d - %m - %Y"), estilo['Parrafo']), Paragraph(agenda.tipo_beneficiario, estilo['Parrafo']),))

        table = Table(data, colWidths=[12*cm, 6*cm])
        table.setStyle(TableStyle([
            ('BOX', (1, 1), (0, 1), 1, colors.black),
            ('BOX', (0, 1), (1, 1), 1, colors.black),
            ('BOX', (1, 3), (0, 3), 1, colors.black),
            ('BOX', (0, 3), (1, 3), 1, colors.black),
            ('BOX', (1, 5), (0, 5), 1, colors.black),
            ('BOX', (0, 5), (1, 5), 1, colors.black),
            ]
        ))
        
        story.append(table)

    def antecedentes(self, story, estilo, agenda):
        data = []
        datastyle = []
        x = 1
        if agenda.antocu:
            data.append((Paragraph("ANTECEDENTES OCULARES", estilo['Titulo']),))
            data.append((Paragraph(agenda.antocu, estilo['Parrafo']),))
            datastyle.append(('BOX', (0, x), (0, x), 1, colors.black))
            x = x + 2
        if agenda.antsis:
            data.append((Paragraph("ANTECEDENTES SISTEMICOS", estilo['Titulo']),))
            data.append((Paragraph(agenda.antsis, estilo['Parrafoj']),))
            datastyle.append(('BOX', (0, x), (0, x), 1, colors.black))
        if data:
            table = Table(data, colWidths=[18*cm])
            table.setStyle(TableStyle(datastyle))
            story.append(table)
    
    def motivoconsulta(self, story, estilo, agenda):
        data = []
        datastyle = []
        x = 1
        if agenda.motivo:
            data.append((Paragraph("MOTIVO DE CONSULTA", estilo['Titulo']),))
            data.append((Paragraph(agenda.motivo, estilo['Parrafoj']),))
            datastyle.append(('BOX', (0, x), (0, x), 1, colors.black))
        if data:
            table = Table(data, colWidths=[18*cm])
            table.setStyle(TableStyle(datastyle))
            story.append(table)

    def agudezavisual(self, story, estilo, agenda):
        data = []
        datastyle = []        
        datastyle.append(('GRID', (2, 1), (5, 5), 1, colors.black))
        datastyle.append(('GRID', (1, 2), (1, 5), 1, colors.black))
        datastyle.append(('SPAN', (0, 0), (5, 0)))
        datastyle.append(('SPAN', (2, 1), (3, 1)))
        datastyle.append(('SPAN', (2, 2), (3, 2)))
        datastyle.append(('SPAN', (2, 3), (3, 3)))
        datastyle.append(('SPAN', (2, 4), (3, 4)))
        datastyle.append(('SPAN', (4, 1), (5, 1)))
        datastyle.append(('SPAN', (4, 2), (5, 2)))
        datastyle.append(('SPAN', (4, 3), (5, 3)))
        datastyle.append(('SPAN', (4, 4), (5, 4)))

        data.append((Paragraph("AGUDEZA VISUAL", estilo['Titulo']),"","","","",""))
        data.append(("", "", Paragraph("O.D.", estilo['Titulo2']), "", Paragraph("O.I.", estilo['Titulo2']), ""))
        data.append(("", Paragraph("S/C", estilo['Titulo']), Paragraph(agenda.dsc, estilo['ParrafoCentro']),"",
                     Paragraph(agenda.isc, estilo['ParrafoCentro']),""))
        data.append(("", Paragraph("C/C", estilo['Titulo']),Paragraph(agenda.dcc, estilo['ParrafoCentro']), "",
                     Paragraph(agenda.icc, estilo['ParrafoCentro']),""))
        refracd = ""
        if agenda.dre1:
            refracd = refracd+agenda.dre1+", "
        else:
            refracd = refracd+"---, "
        if agenda.dre2:
            refracd = refracd+agenda.dre2+", "
        else:
            refracd = refracd+"---, "
        if agenda.dre3:
            refracd = refracd+agenda.dre3+"°"
        else:
            refracd = refracd+"---"
        refraci = ""
        if agenda.ire1:
            refraci = refraci + agenda.ire1 + ", "
        else:
            refraci = refraci + "---, "
        if agenda.ire2:
            refraci = refraci + agenda.ire2 + ", "
        else:
            refraci = refraci + "---, "
        if agenda.ire3:
            refraci = refraci + agenda.ire3 + "°"
        else:
            refraci = refraci + "---"
        data.append(("",Paragraph("Refrac.", estilo['Titulo']),Paragraph(refracd, estilo['ParrafoCentro']), "",
                     Paragraph(refraci, estilo['ParrafoCentro']),""))
        if agenda.ddc2:             
            data.append(("",Paragraph("Cerca", estilo['Titulo']), Paragraph(agenda.ddc1, estilo['ParrafoCentro']), "",
                     Paragraph(agenda.ddc2, estilo['ParrafoCentro']), ""))
            datastyle.append(('SPAN', (2, 5), (3, 5)))
            datastyle.append(('SPAN', (4, 5), (5, 5)))
            datastyle.append(('BOX', (0, 1), (5, 5), 1, colors.black))
        else:
            datastyle.append(('BOX', (0, 1), (5, 4), 1, colors.black))

        table = Table(data, colWidths=[3*cm, 3*cm, 3*cm, 3*cm, 3*cm, 3*cm,])
        table.setStyle(TableStyle(datastyle))
        story.append(table)

    def pio(self, story, estilo, agenda):
        data = []
        datastyle = []
        if (agenda.dto or agenda.ito):
            data.append((Paragraph("PIO", estilo['Titulo']),"",))
            data.append((Paragraph("OD", estilo['Titulo2']),(Paragraph("OI", estilo['Titulo2'])),))
            data.append((Paragraph(agenda.dto, estilo['Parrafoj']),(Paragraph(agenda.ito, estilo['Parrafoj'])),))
            datastyle.append(('GRID', (0, 1), (1, 2), 1, colors.black))
            table = Table(data, colWidths=[9*cm, 9*cm])
            table.setStyle(TableStyle(datastyle))
            story.append(table)
    
    def bio(self, story, estilo, agenda):
        data = []
        datastyle = []
        if (agenda.dbio or agenda.ibio):
            data.append((Paragraph("BIOMICROSCOPIA", estilo['Titulo']),"",))
            data.append((Paragraph("OD", estilo['Titulo2']),(Paragraph("OI", estilo['Titulo2'])),))
            data.append((Paragraph(agenda.dbio, estilo['Parrafoj']),(Paragraph(agenda.ibio, estilo['Parrafoj'])),))
            datastyle.append(('GRID', (0, 1), (1, 2), 1, colors.black))
            table = Table(data, colWidths=[9*cm, 9*cm])
            table.setStyle(TableStyle(datastyle))
            story.append(table)
    def fdo(self, story, estilo, agenda):
        data = []
        datastyle = []
        if (agenda.dfdo or agenda.ifdo):
            data.append((Paragraph("FONDO DE OJO", estilo['Titulo']),"",))
            data.append((Paragraph("OD", estilo['Titulo2']),(Paragraph("OI", estilo['Titulo2'])),))
            data.append((Paragraph(agenda.dfdo, estilo['Parrafoj']),(Paragraph(agenda.ifdo, estilo['Parrafoj'])),))
            datastyle.append(('GRID', (0, 1), (1, 2), 1, colors.black))
            table = Table(data, colWidths=[9*cm, 9*cm])
            table.setStyle(TableStyle(datastyle))
            story.append(table)

    def otros(self, story, estilo, agenda):
        data = []
        datastyle = []
        x = 1
        if agenda.otros:
            data.append((Paragraph("OTROS", estilo['Titulo']),))
            data.append((Paragraph(agenda.otros, estilo['Parrafoj']),))
            datastyle.append(('BOX', (0, x), (0, x), 1, colors.black))
            table = Table(data, colWidths=[18*cm])
            table.setStyle(TableStyle(datastyle))
            story.append(table)

    def diagnosticos(self, story, estilo, agenda):
        data = []
        datastyle = []
        diagnosticos = ''
        x = 1
        for idx, item in enumerate(agenda.diagnostico_set.all()):
            diagnosticos = diagnosticos + str(idx + 1) + '.- ' + item.detalle + ', '
        if diagnosticos:
            data.append((Paragraph("DIAGNOSTICO", estilo['Titulo']),))
            data.append((Paragraph(diagnosticos, estilo['Parrafo']),))
            datastyle.append(('BOX', (0, x), (0, x), 1, colors.black))
            table = Table(data, colWidths=[18*cm])
            table.setStyle(TableStyle(datastyle))
            story.append(table)

    def tratamientos(self, story, estilo, agenda):
        data = []
        datastyle = []
        tratamientos = ''
        x = 1
        for idx, item in enumerate(agenda.tratamiento_set.all()):
            tratamientos = tratamientos + str(idx + 1) + '.- ' + item.detalle + ', '
        if tratamientos:
            data.append((Paragraph("TRATAMIENTO", estilo['Titulo']),))
            data.append((Paragraph(tratamientos, estilo['Parrafo']),))
            datastyle.append(('BOX', (0, x), (0, x), 1, colors.black))
            table = Table(data, colWidths=[18*cm])
            table.setStyle(TableStyle(datastyle))
            story.append(table)        

    def get(self, *args, **kwargs):
        agenda = Agenda.objects.get(id=self.kwargs['pk'])
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "receta.pdf"  # llamado clientes
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name
        buffer = BytesIO()
        doc = BaseDocTemplate(buffer, pagesize=letter)
        frame0 = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, showBoundary=0, id='normalBorde')
        doc.addPageTemplates([
            PageTemplate(id='principal', frames=frame0, onPage=self.encabezado),
            ])
        estilo=getSampleStyleSheet()
        estilo.add(ParagraphStyle(name = "Tituloc",  alignment=TA_CENTER, fontSize=18, leading=22, fontName="Helvetica-Bold"))
        estilo.add(ParagraphStyle(name = "Titulo",  alignment=TA_LEFT, fontSize=10, fontName="Helvetica-Bold"))
        estilo.add(ParagraphStyle(name = "Titulo2",  alignment=TA_CENTER, fontSize=10, fontName="Helvetica-Bold"))
        estilo.add(ParagraphStyle(name = "Parrafo",  alignment=TA_LEFT, fontSize=8, fontName="Helvetica"))
        estilo.add(ParagraphStyle(name="ParrafoCentro", alignment=TA_CENTER, fontSize=8, fontName="Helvetica"))
        estilo.add(ParagraphStyle(name = "Parrafoj", alignment=TA_JUSTIFY, fontSize=8, fontName="Helvetica"))

        story = []
        
        story.append(Paragraph("HISTORIA CLINICA", estilo['Tituloc']))
        self.cabecera(story, estilo, agenda)
        self.antecedentes(story, estilo, agenda)
        self.motivoconsulta(story, estilo, agenda)
        self.agudezavisual(story, estilo, agenda)
        self.pio(story, estilo, agenda)
        self.bio(story, estilo, agenda)
        self.fdo(story, estilo, agenda)
        self.otros(story, estilo, agenda)
        self.diagnosticos(story, estilo, agenda)
        self.tratamientos(story, estilo, agenda)
        doc.build(story)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response