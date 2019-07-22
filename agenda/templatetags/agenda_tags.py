from django import template
from datetime import date
from dateutil import relativedelta
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='ctipo')
def ctipo(value):
  DOCUMENTO_CHOICE = {
    0: 'LEVE',
    1: 'MODERADO',
    2: 'URGENTE'
  }
  return DOCUMENTO_CHOICE[value]

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False