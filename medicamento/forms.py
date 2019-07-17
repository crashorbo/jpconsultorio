from django import forms
from .models import Medicamento

class MedicamentoForm(forms.ModelForm):
  class Meta:
    model = Medicamento
    fields = ('nombre', 'presentacion','indicacion')

    widgets = {
      'nombre': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'presentacion': forms.Select(attrs={'class': 'form-control form-control-sm'}),
      'indicacion': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2})
    }