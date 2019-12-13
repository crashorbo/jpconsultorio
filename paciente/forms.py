from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Paciente, Archivopdf, Nota

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
      'paciente': forms.HiddenInput(),
      'fecha_documento': forms.DateInput(attrs={'class': 'form-control form-control-sm fecha'}),
      'nombre': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'descripcion': CKEditorWidget(),
      'archivo': forms.FileInput(attrs={'class': 'dropify'}),
    }

class NotaForm(forms.ModelForm):
  class Meta:
    model = Nota
    fields = ('paciente', 'fecha_documento', 'tipo', 'nombre', 'texto')

    widgets = {
      'paciente': forms.HiddenInput(),
      'fecha_documento': forms.DateInput(attrs={'class': 'form-control form-control-sm fecha'}),
      'nombre': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'texto': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2}),
      'tipo': forms.Select(attrs={'class': 'form-control'}),
    }