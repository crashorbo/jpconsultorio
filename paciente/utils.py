import dataset
import os
from pathlib import Path
from dbfread import DBF
from django.conf import settings
from core.models import Recpaciente
from paciente.models import Paciente
from datetime import datetime


def migrarpacientes():
  pacientes = Recpaciente.objects.all()
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