from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
  class Meta:
    model = Paciente
    fields = ('nombres', 'apellidos', 'fecha_nacimiento', 'documento', 'nro_documento', 'direccion', 'telefono', 'ocupacion')

    widgets = {
      'nombres': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombres'}),
      'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
      'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control fecha'}),
      'documento': forms.Select(attrs={'class': 'form-control'}),
      'nro_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numero Documento'}),
      'ocupacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ocupacion'}),
      'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono'}),
      'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Direccion'}),
    }