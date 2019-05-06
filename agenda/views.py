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
from io import BytesIO
from decimal import Decimal, getcontext

from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.graphics.shapes import Drawing 
from reportlab.graphics.barcode.qr import QrCodeWidget 
from reportlab.graphics import renderPDF
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
        qs = Agenda.objects.filter(estado__exact=0)
        qs = self.get_results(qs)
        return HttpResponse({
            json.dumps(qs)
        }, content_type='application/json')

    def get_results(self, results):
        TIPO_CHOICE = {
            0: 'bg-success',
            1: 'bg-danger',
        }
        return [dict(id=x.id,title=x.paciente.nombres+' '+x.paciente.apellidos, start=x.fecha.strftime("%Y-%m-%d" )+' '+x.hora_inicio.strftime("%H:%M:%S"), end=x.fecha.strftime("%Y-%m-%d" )+' '+x.hora_fin.strftime("%H:%M:%S"), className=TIPO_CHOICE[self.calculo(x)]) for x in results]

    def calculo(self, objeto):
        valor = 0
        for item in objeto.agendaserv_set.all():
            if not item.estado:
                valor = valor + item.costo
        if valor > 0:
            return 1
        else:
            return 0

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
        return render(self.request, 'agenda/ajax/tratamientos.html', context={ 'consulta': consulta })

class DiagnosticoListar(ListView):
    template_name = 'agenda/diaglistar.html'
    
    def get_queryset(self, *args, **kwargs):
        self.agenda = get_object_or_404(Agenda, pk=self.kwargs['pk'])
        return Diagnostico.objects.filter(agenda=self.agenda)

class AgendaservUpdate(View):
    def get(self, *args, **kwargs):
        servicio = Agendaserv.objects.get(id=self.kwargs['pk'])
        servicio.estado = True
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
                                pagesize=landscape(letter),
                                rightMargin=30,
                                leftMargin=30,
                                topMargin=30,
                                bottomMargin=30,
                                )

        cabeza = ParagraphStyle(name="cabeza", alignment=TA_LEFT, fontSize=14, fontName="Times-Roman", textColor=colors.darkblue)
        cabecera = ParagraphStyle(name="cabecera", alignment=TA_CENTER, fontSize=12, fontName="Times-Roman", textColor=colors.white)
        celdaderecha = ParagraphStyle(name="celdaderecha",alignment=TA_RIGHT, fontsize=10, fontName="Times-Roman")
        celdaderechabold = ParagraphStyle(name="celdaderecha",alignment=TA_RIGHT, fontsize=12, fontName="Times-Bold")
        celda = ParagraphStyle(name="celda", alignment=TA_LEFT, fontsize=10, fontName="Times-Roman")
        celdabold = ParagraphStyle(name="celda", alignment=TA_LEFT, fontsize=12, fontName="Times-Bold")
        celdaverde = ParagraphStyle(name="celdaverde", alignment=TA_CENTER, fontSize=8, fontName="Times-Roman", textColor=colors.green)
        celdaroja = ParagraphStyle(name="celdaroja", alignment=TA_CENTER, fontSize=8, fontName="Times-Roman", textColor=colors.red)
        celdarojarem = ParagraphStyle(name="celdaroja", alignment=TA_CENTER, fontSize=8, fontName="Times-Roman", textColor=colors.red, backColor = colors.yellow)
        celdaremarcada = ParagraphStyle(name="celda", alignment=TA_LEFT, fontsize=8, fontName="Times-Roman", backColor = colors.yellow)                                
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER, fontSize=16))
        styles.add(ParagraphStyle(name='subtitulo', alignment=TA_LEFT, fontSize=14))
        header = Paragraph("Reporte Movimientos "+hoy.strftime("%d/%m/%Y"), styles['centered'])
        subparticular = Paragraph("Particulares:", styles['Heading2'])
        subasegurados = Paragraph("Asegurados:", styles['Heading2'])
        movimiento = []
        particulares = []
        asegurados = []
        seguro = []
        total_particular_costo = 0
        total_particular_cobrado = 0
        total_asegurado_costo = 0
        movimiento.append(header)
        movimiento.append(subparticular)
        
        items = Agendaserv.objects.filter(fecha=datetime.strptime(hoy.strftime("%Y-%m-%d"), "%Y-%m-%d"))
        for item in items:
            if not item.agenda.tipo:
                if item.estado:
                    aux = item.costo
                    total_particular_cobrado = total_particular_cobrado + item.costo
                else:
                    aux = Decimal('0.00')
                this_particular = [Paragraph((item.agenda.paciente.nombres + ' ' + item.agenda.paciente.apellidos), celda), Paragraph(item.servicio.nombre, celda), Paragraph(str(item.costo), celdaderecha), Paragraph(str(aux),celdaderecha)]
                particulares.append(this_particular)
                total_particular_costo = total_particular_costo + item.costo
            else:
                this_asegurado = [Paragraph((item.agenda.paciente.nombres + ' ' + item.agenda.paciente.apellidos), celda), Paragraph(item.servicio.nombre, celda), Paragraph(str(item.agenda.matricula), celda), Paragraph(item.agenda.tipo_beneficiario, celda), Paragraph(str(item.costo),celdaderecha)]
                asegurados.append(this_asegurado)
                total_asegurado_costo = total_asegurado_costo + item.costo
        this_particular = [Paragraph('TOTAL', celdabold), Paragraph('', celda), Paragraph(str(total_particular_costo), celdaderechabold), Paragraph(str(total_particular_cobrado),celdaderechabold)]
        particulares.append(this_particular)
        this_asegurado = [Paragraph('TOTAL', celdabold), Paragraph('', celda), Paragraph('', celda), Paragraph('', celda), Paragraph(str(total_asegurado_costo),celdaderechabold)]
        asegurados.append(this_asegurado)
        
        headings = (Paragraph('Nombre', cabecera), Paragraph('Consulta', cabecera), Paragraph('Costo', cabecera), Paragraph('SubTotal',cabecera))
        t1 = Table([headings] + particulares, colWidths=[11 * cm, 8 * cm, 3 * cm, 3 * cm])
        t1.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.black)
        ]
        ))

        headings = (Paragraph('Nombre', cabecera), Paragraph('Consulta', cabecera), Paragraph('matricula', cabecera), Paragraph('Procede', cabecera), Paragraph('Costo',cabecera))
        t2 = Table([headings] + asegurados, colWidths=[9 * cm, 7 * cm, 4 * cm, 2 * cm, 3 * cm])
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