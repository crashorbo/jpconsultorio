from django import template
from datetime import date
from dateutil import relativedelta

register = template.Library()

@register.filter(name='documento')
def documento(value):
  DOCUMENTO_CHOICE = {
    1: 'CEDULA DE IDENTIDAD',
    2: 'PASAPORTE',
    3: 'CERTIFICADO DE NACIMIENTO'
  }

  return DOCUMENTO_CHOICE[value]

@register.filter(name='edad')
def edad(value):
  hoy = date.today()
  edad = hoy.year - value.year - ((hoy.month, hoy.day) < (value.month, value.day))

  if edad > 0:
    return str(edad)+' AÑOS'
  else:
    meses = relativedelta.relativedelta(hoy, value)
    return str(meses.months)+' MESES'
  return edad
