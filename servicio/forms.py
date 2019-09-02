from django import forms
from .models import Servicio

class ServicioForm(forms.ModelForm):
  class Meta:
    model = Servicio
    fields = ('nombre', 'costo')

    widgets = {
      'nombre': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'costo': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
    }
