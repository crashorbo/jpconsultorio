from django import forms
from .models import Paciente, Archivopdf

class PacienteForm(forms.ModelForm):
  class Meta:
    model = Paciente
    fields = ('nombres', 'apellidos', 'fecha_nacimiento', 'documento', 'nro_documento', 'direccion', 'telefono', 'ocupacion')

    widgets = {
      'nombres': forms.TextInput(attrs={'class': 'form-control'}),
      'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
      'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control fecha'}),
      'documento': forms.Select(attrs={'class': 'form-control'}),
      'nro_documento': forms.TextInput(attrs={'class': 'form-control'}),
      'ocupacion': forms.TextInput(attrs={'class': 'form-control'}),
      'telefono': forms.TextInput(attrs={'class': 'form-control'}),
      'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
    }

class ArchivopdfForm(forms.ModelForm):
  class Meta:
    model = Archivopdf
    fields = ('paciente', 'fecha_documento', 'archivo', 'nombre', 'descripcion')

    widgets = {
      'fecha_documento': forms.DateInput(attrs={'class': 'form-control fecha'}),
      'nombre': forms.TextInput(attrs={'class': 'form-control'}),
      'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
      'archivo': forms.FileInput(attrs={'class': 'dropify'}),
    }