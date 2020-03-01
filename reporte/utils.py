import os
from django.conf import settings
from django.http import HttpResponse
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
from io import BytesIO

from .models import Reporteseguro
from agenda.models import Agendaserv
from .models import Reporteseguro
from .templatetags import reporte_tag


class ReportePdfSeguro:
    def __init__(self, id_reporte_seguro):
        self.id_reporte_seguro = id_reporte_seguro

    def __encabezado(self, canvas, doc):
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

    def __detalle(self, story, estilo, reportes):
        data = []
        datastyle = []
        data.append((Paragraph("NRO", estilo['Titulo']), Paragraph("PACIENTE", estilo['Titulo']), Paragraph("FECHA", estilo['Titulo']),\
                     Paragraph("DETALLE", estilo['Titulo']), Paragraph("COSTO", estilo['Titulo'])))
        datastyle.append(('GRID', (0, 0), (6, -1), 1, colors.black))
        suma = 0
        for index, reporte in enumerate(reportes):
            data.append(
                (
                    Paragraph("{}".format(index+1), estilo['Titulo']),
                    Paragraph("{} {}".format(reporte.agenda.paciente.nombres, reporte.agenda.paciente.apellidos), estilo['Parrafo']),
                    Paragraph("{}".format((reporte.fecha).strftime("%d/%m/%Y")), estilo['Parrafoc']),
                    Paragraph("{}".format(reporte.servicio.nombre), estilo['Parrafo']),
                    Paragraph("{}".format(reporte.costo), estilo['Parrafod'])
                )
            )
            suma = suma + reporte.costo
        data.append(
            (
                Paragraph("", estilo['Titulo']),
                Paragraph("", estilo['Titulo']),
                Paragraph("", estilo['Titulo']),
                Paragraph("TOTAL", estilo['Titulo']),
                Paragraph("{}".format(suma), estilo['Titulod']),
            )
        )
        table = Table(data, colWidths=[1.5*cm, 7*cm, 3*cm, 5*cm, 2.5*cm])
        table.setStyle(TableStyle(datastyle))
        story.append(table)

    def generar_reporte(self):
        reporte_seguro = Reporteseguro.objects.get(id=self.id_reporte_seguro)
        print("{} {} {}".format(reporte_seguro.gestion, reporte_seguro.mes, reporte_seguro.id))
        agenda_servicio = Agendaserv.objects.filter(fecha__year=reporte_seguro.gestion, fecha__month=reporte_seguro.mes,
                                                    agenda__tipo=1, agenda__seguro=reporte_seguro.seguro.id, agenda__deleted=False)
        print(len(agenda_servicio))
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "informe_{}-{}-{}.pdf".format(reporte_seguro.seguro.nombre, reporte_seguro.gestion, reporte_seguro.mes)  # llamado clientes
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name
        buffer = BytesIO()
        doc = BaseDocTemplate(buffer, pagesize=letter)
        frame0 = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, showBoundary=0, id='normalBorde')
        doc.addPageTemplates([
            PageTemplate(id='principal', frames=frame0, onPage=self.__encabezado),
        ])
        estilo = getSampleStyleSheet()
        estilo.add(ParagraphStyle(name="Titulo", alignment=TA_CENTER, fontSize=10, fontName="Helvetica-Bold"))
        estilo.add(ParagraphStyle(name="Titulod", alignment=TA_RIGHT, fontSize=10, fontName="Helvetica-Bold"))
        estilo.add(ParagraphStyle(name="Parrafo", alignment=TA_JUSTIFY, fontSize=8, fontName="Helvetica"))
        estilo.add(ParagraphStyle(name="Parrafod", alignment=TA_RIGHT, fontSize=8, fontName="Helvetica"))
        estilo.add(ParagraphStyle(name="Parrafoc", alignment=TA_CENTER, fontSize=8, fontName="Helvetica"))
        estilo.add(ParagraphStyle(name="Tituloc1", alignment=TA_CENTER, fontSize=14, leading=22, fontName="Helvetica-Bold"))
        estilo.add(ParagraphStyle(name="Tituloc2", alignment=TA_CENTER, fontSize=12, leading=22, fontName="Helvetica-Bold"))
        story = []
        story.append(Paragraph("{}".format(reporte_seguro.seguro.nombre), estilo['Tituloc1']))
        story.append(Paragraph("{}-{}".format(reporte_tag.mesliteral(reporte_seguro.mes), reporte_seguro.gestion), estilo['Tituloc2']))
        self.__detalle(story, estilo, agenda_servicio)
        doc.build(story)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
