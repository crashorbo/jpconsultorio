import json
import locale
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View, CreateView, ListView, UpdateView, DeleteView, DetailView
from dal import autocomplete
from django.db.models import Q
from datetime import datetime, timedelta
from django.urls import reverse
from django.db import transaction
from datetime import date, datetime
from django.utils.dateparse import parse_date
# Create your views here.
from paciente.models import Paciente
from configuracion.models import Tipolente
from core.models import Movdiario
from .models import Agenda, Diagnostico, Tratamiento, Agendaserv, Receta
from .forms import AgendaForm, DiagnosticoForm, TratamientoForm, ServicioFormset, RecetaForm
from io import BytesIO
from decimal import Decimal, getcontext
from django.utils import formats
import textwrap

from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter, landscape, portrait
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

class AgendaFechaListar(View):
    def get(self, *args, **kwargs):
        q = self.request.GET['fecha']
        fecha = datetime.strptime(q, "%d-%m-%Y")
        qs = Agenda.objects.filter(fecha=fecha)       
        return render(self.request, 'agenda/ajax/listaconsultas.html', {'consultas': qs})

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
        borrar = self.get_object()
        print(borrar.estado)
        if not borrar.estado: 
            borrar.delete()
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
        receta = RecetaForm(initial=diag_data)
        tipolentes = Tipolente.objects.all()
        context['tipolentes'] = tipolentes
        context['diagform'] = diagnostico
        context['tratform'] = tratamiento
        context['recetaform'] = receta
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
        historias = self.model.objects.filter(paciente__exact=self.kwargs['pk'], estado__exact=1).order_by('-fecha')
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

class Reporterec(View):
    def subrayar(self, pdf, x, y, texto):
        tam = len(texto)
        pdf.line(x-tam*4, y-4,x+tam*4,y-4)
    
    def subrayar2(self, pdf, x, y, texto):
        tam = len(texto)
        pdf.line(x, y-4,x+tam*8,y-4)

    def paciente(self, pdf):
        pdf.setFont("Times-Bold", 12)
        pdf.drawCentredString(220,430, self.agenda.paciente.nombres + ' ' + self.agenda.paciente.apellidos)
        self.subrayar(pdf, 220,430,self.agenda.paciente.nombres + ' ' +self.agenda.paciente.apellidos)

    def encabezado(self, pdf):
        pdf.setFont("Times-Bold", 12)
        pdf.drawCentredString(220,400, "RECETA DE LENTES")
        self.subrayar(pdf, 220,400, "RECETA DE LENTES")

    def subtitulo(self, pdf):
        pdf.setFont("Times-Bold", 12)
        if (self.agenda.adicion):
            pdf.drawString(65,370, "PARA LEJOS:")
            self.subrayar2(pdf, 65,370, "PARA LEJOS")
        else:
            pdf.drawString(65,370, "USO PERMANENTE:")
            self.subrayar2(pdf, 65,370, "USO PERMANENTE")

    def medida(self,pdf):
        if (self.agenda.impav):
            pdf.setFont("Times-Bold", 16)
            pdf.drawCentredString(85,305, "OD.")
            pdf.drawCentredString(85,275, "OI.")
            pdf.setFont("Times-Roman", 12)
            pdf.drawCentredString(140,335, "ESFERICO")
            pdf.drawCentredString(215,335, "CILINDRICO")
            pdf.drawCentredString(295,335, "EJE")
            pdf.drawCentredString(363,335, "A.V.")
            pdf.drawString(65, 255, "Favor Medir D.P.")
            pdf.setFont("Times-Roman", 16)
            if(self.agenda.drc1):
                pdf.drawCentredString(140,305, self.agenda.drc1)
            else:
                pdf.drawCentredString(140,305, '------')
            if(self.agenda.drc2):
                pdf.drawCentredString(215,305, self.agenda.drc2)
            else:
                pdf.drawCentredString(215,305, '------')
            if(self.agenda.irc1):
                pdf.drawCentredString(140,275, self.agenda.irc1)
            else:
                pdf.drawCentredString(140,275, '------')
            if(self.agenda.irc2):
                pdf.drawCentredString(215,275, self.agenda.irc2)
            else:
                pdf.drawCentredString(215,275, '------')
            pdf.setFont("Times-Bold", 16)
            if(self.agenda.drc3):
                pdf.drawCentredString(295,305, self.agenda.drc3+'°')
            else:
                pdf.drawCentredString(295,305, '------')
            if(self.agenda.irc3):
                pdf.drawCentredString(295,275, self.agenda.irc3+'°')
            else:
                pdf.drawCentredString(295,275, '------')
            pdf.setFont("Times-Roman", 16)
            if(self.agenda.dcc):
                pdf.drawCentredString(363,305, '20/'+self.agenda.dcc)
            else:
                pdf.drawCentredString(363,305, '------')
            if(self.agenda.irc3):
                pdf.drawCentredString(363,275, '20/'+self.agenda.icc)
            else:
                pdf.drawCentredString(363,275, '------')
        else:
            pdf.setFont("Times-Bold", 16)
            pdf.drawCentredString(100,305, "OD.")
            pdf.drawCentredString(100,275, "OI.")
            pdf.setFont("Times-Roman", 12)
            pdf.drawCentredString(160,335, "ESFERICO")
            pdf.drawCentredString(240,335, "CILINDRICO")
            pdf.drawCentredString(320,335, "EJE")
            pdf.drawString(80, 255, "Favor Medir D.P.")
            pdf.setFont("Times-Roman", 16)
            if(self.agenda.drc1):
                pdf.drawCentredString(160,305, self.agenda.drc1)
            else:
                pdf.drawCentredString(160,305, '------')
            if(self.agenda.drc2):
                pdf.drawCentredString(240,305, self.agenda.drc2)
            else:
                pdf.drawCentredString(240,305, '------')
            if(self.agenda.irc1):
                pdf.drawCentredString(160,275, self.agenda.irc1)
            else:
                pdf.drawCentredString(160,275, '------')
            if(self.agenda.irc2):
                pdf.drawCentredString(240,275, self.agenda.irc2)
            else:
                pdf.drawCentredString(240,275, '------')
            pdf.setFont("Times-Bold", 16)
            if(self.agenda.drc3):
                pdf.drawCentredString(320,305, self.agenda.drc3+'°')
            else:
                pdf.drawCentredString(320,305, self.agenda.drc3+'------')
            if(self.agenda.irc3):
                pdf.drawCentredString(320,275, self.agenda.irc3+'°')
            else:
                pdf.drawCentredString(320,275, '------')
        
    def observaciones(self, pdf, y):
        adicion = self.agenda.tipo_lente.split(",")
        pdf.setFont("Times-Bold", 12)
        pdf.drawString(80, y, "Obs.")
        pdf.setFont("Times-Roman", 10)
        pdf.setFillColorRGB(1,0,0)
        for item in adicion:
            pdf.drawString(140, y, item)
            y = y - 15
        y = y - 5
        pdf.setFillColorRGB(0,0,0)
        pdf.drawString(80, y, "No olvide traer sus lentes a control.")
        pdf.drawString(80, y-15, "No olvide traer su receta en la proxima consulta.")
        mes = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
        pdf.drawString(80, 50, str(date.today().day)+" - "+mes[date.today().month]+" - "+str(date.today().year))
        pdf.drawRightString(360, 50, datetime.now().strftime("(%H:%M:%S)"))

    def tabla(self, pdf):
        if (self.agenda.impav):
            pdf.line(65, 350 ,390, 350)
            pdf.line(65, 325 ,390, 325)
            pdf.line(65, 295 ,390, 295)
            pdf.line(65, 265 ,390, 265)
            pdf.line(65, 350 ,65, 265)
            pdf.line(105, 350 ,105, 265)
            pdf.line(175, 350 ,175, 265)
            pdf.line(255, 350 ,255, 265)
            pdf.line(335, 350 ,335, 265)
            pdf.line(390, 350 ,390, 265)
        else:
            pdf.line(80, 350 ,360, 350)
            pdf.line(80, 325 ,360, 325)
            pdf.line(80, 295 ,360, 295)
            pdf.line(80, 265 ,360, 265)
            pdf.line(80, 350 ,80, 265)
            pdf.line(120, 350 ,120, 265)
            pdf.line(200, 350 ,200, 265)
            pdf.line(280, 350 ,280, 265)
            pdf.line(360, 350 ,360, 265)

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
        pdf.drawCentredString(220,430, self.agenda.paciente.nombres + ' ' + self.agenda.paciente.apellidos)
        self.subrayar(pdf, 220,430,self.agenda.paciente.nombres + ' ' +self.agenda.paciente.apellidos)
        pdf.setFont("Times-Roman", 10)
        mes = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
        pdf.drawString(80, 50, str(date.today().day)+" - "+mes[date.today().month]+" - "+str(date.today().year))
        pdf.drawRightString(360, 50, datetime.now().strftime("(%H:%M:%S)"))

    def receta(self, pdf, numero, rec):
        pdf.setFont("Times-Bold", 16)
        pdf.drawString(80, self.y, str(numero)+'.- '+rec.medicamento.nombre)
        pdf.setFont("Times-Bold", 12)
        pdf.setFillColorRGB(1,0,0)
        pdf.drawRightString(360, self.y, '('+rec.presentacion+')')
        self.y = self.y - 20
        pdf.drawRightString(360, self.y, '#'+str(rec.cantidad))
        pdf.setFillColorRGB(0,0,0)
        pdf.setFont("Times-Roman", 12)
        texto = textwrap.wrap(rec.indicacion, 50)
        self.y = self.y - 20
        pdf.setFont("Times-Bold", 12)
        pdf.drawString(100, self.y, ">")
        pdf.setFont("Times-Roman", 12)
        x = 0
        for item in texto:            
            pdf.drawString(115, self.y, texto[x])
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
        for item in self.agenda.receta_set.all():
            self.receta(pdf, indice, item)
            self.y = self.y-30
            indice = indice+1
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response