import dataset
import os
from pathlib import Path
from dbfread import DBF
import dataset
from django.conf import settings
from core.models import RecPaciente, RecHistoria, RecDiagnostico, RecTratamiento
from paciente.models import Paciente
from agenda.models import Agenda, Diagnostico, Tratamiento
from seguro.models import Seguro
from datetime import datetime

def crearpacientes():
  db = dataset.connect('postgresql://postgres:add150806@localhost:5432/consultorio')
  table = db['rec_paciente']

  for record in DBF('historial/paciente.dbf'):
    table.insert(record)

def crearhistorial():
  db = dataset.connect('postgresql://postgres:add150806@localhost:5432/consultorio')
  table = db['rec_historia']

  for record in DBF('historial/ficha.dbf'):
    table.insert(record)

def createtratamientos():
  db = dataset.connect('postgresql://postgres:add150806@localhost:5432/consultorio')
  table = db['rec_tratamiento']

  for record in DBF('historial/tratam.dbf'):
    table.insert(record)

def creatediagnosticos():
  db = dataset.connect('postgresql://postgres:add150806@localhost:5432/consultorio')
  table = db['rec_diagnostico']

  for record in DBF('historial/diagnos.dbf'):
    table.insert(record)

def migrarpacientes():
  pacientes = RecPaciente.objects.all()
  now = datetime.now()
  fecha = now.strftime("%Y-%m-%d")
  print(fecha)
  for paciente in pacientes:
    if paciente.fecha_nac is None:
      sispaciente = Paciente(nombres=paciente.nombres, apellidos=paciente.a_paterno+' '+paciente.a_materno,fecha_nacimiento=datetime.strptime(fecha, "%Y-%m-%d"), documento=1, nro_documento=paciente.ci, direccion=paciente.direccion, telefono=paciente.telefono, ocupacion=paciente.ocupacion, codigo=paciente.codigo)
      sispaciente.save()
    else:
      sispaciente = Paciente(nombres=paciente.nombres, apellidos=paciente.a_paterno+' '+paciente.a_materno,fecha_nacimiento=paciente.fecha_nac, documento=1, nro_documento=paciente.ci, direccion=paciente.direccion, telefono=paciente.telefono, ocupacion=paciente.ocupacion, codigo=paciente.codigo)
      sispaciente.save()
  return len(pacientes)

def migrarhistorias():
  historias = RecHistoria.objects.all()
  now = datetime.now()
  fecha = now.strftime("%Y-%m-%d")
  seguro = Seguro.objects.get(id=1)
  for historia in historias:
    try:
      paciente = Paciente.objects.get(codigo=historia.paciente)
      sishistoria = Agenda(paciente=paciente, seguro=seguro, fecha=historia.fecha, estado=1, procedencia=historia.procedenc, antocu=historia.oculares, antsis=historia.sitemicos, motivo=historia.mot_consul, dsc=historia.av_od1, dcc=historia.av_od2, dre1=historia.av_od3a, dre2=historia.av_od3b, dre3=historia.av_od3c, dau=historia.av_od4, ddc1=historia.av_od5, ddc2=historia.av_od6, dph=historia.av_od7, dci=historia.av_od8, dcl=historia.av_od9, drc1=historia.av_od10a, drc2=historia.av_od10b, drc3=historia.av_od10c, isc=historia.av_oi1, icc=historia.av_oi2, ire1=historia.av_oi3a, ire2=historia.av_oi3b, ire3=historia.av_oi3c, iau=historia.av_oi4, idc1=historia.av_oi5, idc2=historia.av_oi6, iph=historia.av_oi7, ici=historia.av_oi8, icl=historia.av_oi9, irc1=historia.av_oi10a, irc2=historia.av_oi10b, irc3=historia.av_oi10c, adicion=historia.adicion, dto=historia.to_od, ito=historia.to_oi, dbio=historia.biom_od, ibio=historia.biom_oi, dfdo=historia.fondo_od, ifdo=historia.fondo_oi, otros=historia.otros, tipo_lente=historia.recet, codigo=historia.codigo )
      sishistoria.save()
    except Exception as e:      
      print(e)
  return len(historias)

def migrardiagnosticos():
  diagnosticos = RecDiagnostico.objects.all()
  for diagnostico in diagnosticos:
    try:
      agenda = Agenda.objects.get(codigo=diagnostico.cod)
      sisdiagnostico = Diagnostico(agenda=agenda, detalle=diagnostico.detalle)
      sisdiagnostico.save()
    except Exception as e:      
      print(e)
  return len(diagnosticos)

def migrartratamientos():
  tratamientos = RecTratamiento.objects.all()
  for tratamiento in tratamientos:
    try:
      agenda = Agenda.objects.get(codigo=tratamiento.cod)
      sistratamiento = Tratamiento(agenda=agenda, detalle=tratamiento.detalle)
      sistratamiento.save()
    except Exception as e:      
      print(e)
  return len(tratamientos)

def fechaconsulta():
  historias = Agenda.objects.all()
  for item in historias:
    item.fecha_consulta = item.fecha
    item.save()