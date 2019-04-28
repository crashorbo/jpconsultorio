from django import template
from datetime import date
from dateutil import relativedelta

register = template.Library()

@register.filter(name='ctipo')
def ctipo(value):
  DOCUMENTO_CHOICE = {
    0: 'LEVE',
    1: 'MODERADO',
    2: 'URGENTE'
  }
  return DOCUMENTO_CHOICE[value]