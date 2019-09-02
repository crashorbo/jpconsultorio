from django import forms
from .models import Tipolente

class TipolenteForm(forms.ModelForm):
  class Meta:
    model = Tipolente
    fields = ('nombre', 'descripcion')

    widgets = {
      'nombre': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'descripcion': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2}),
    }