from django import forms
from django.forms.models import inlineformset_factory
from .models import Agenda, Diagnostico, Tratamiento, Agendaserv
from dal import autocomplete
from paciente.models import Paciente
from seguro.models import Seguro
from servicio.models import Servicio

class AgendaForm(forms.ModelForm):
  paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), empty_label="Seleccionar Paciente", widget=autocomplete.ModelSelect2(url='paciente-autocomplete'))
  seguro = forms.ModelChoiceField(queryset=Seguro.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
  
  class Meta:
    model = Agenda
    fields = ('paciente', 'seguro', 'fecha', 'hora_inicio', 'hora_fin', 'tipo', 'prioridad', 'procedencia', 'matricula', 'tipo_beneficiario', 'antocu', 'antsis', 'motivo', 'dsc', 'dcc', 'dre1', 'dre2', 'dre3', 'dau', 'ddc1', 'ddc2', 'dph', 'dci', 'dcl', 'drc1', 'drc2', 'drc3', 'isc', 'icc', 'ire1', 'ire2', 'ire3', 'iau', 'idc1', 'idc2', 'iph', 'ici', 'icl', 'irc1', 'irc2', 'irc3', 'adicion', 'tipo_lente', 'dto', 'ito', 'dbio', 'ibio', 'dfdo', 'ifdo', 'otros')

    widgets = {
      'fecha': forms.DateInput(attrs={'class': 'form-control fecha', 'placeholder': 'Fecha'}),
      'hora_inicio': forms.TimeInput(format='%H:%M', attrs={'class': 'form-control clockpicker', 'placeholder': 'Hora','data-placement':'bottom', 'data-align':'top', 'data-autoclose':'true'}),
      'hora_fin': forms.TimeInput(format='%H:%M', attrs={'class': 'form-control clockpicker', 'placeholder': 'Hora', 'data-placement':'bottom', 'data-align':'top', 'data-autoclose':'true'}),
      'tipo': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo'}),
      'prioridad': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Prioridad'}),
      'procedencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Procedencia'}),
      'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matricula'}),
      'tipo_beneficiario': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo Beneficiario'}),
      'antocu': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
      'antsis': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
      'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
      'dsc': forms.TextInput(attrs={'class': 'form-control'}), 
      'dcc': forms.TextInput(attrs={'class': 'form-control'}), 
      'dre1': forms.TextInput(attrs={'class': 'form-control'}), 
      'dre2': forms.TextInput(attrs={'class': 'form-control'}),
      'dre3': forms.TextInput(attrs={'class': 'form-control'}),
      'dau': forms.TextInput(attrs={'class': 'form-control'}),
      'ddc1': forms.Select(attrs={'class': 'form-control'}),
      'ddc2': forms.TextInput(attrs={'class': 'form-control'}),
      'dph': forms.TextInput(attrs={'class': 'form-control'}),
      'dci': forms.TextInput(attrs={'class': 'form-control'}),
      'dcl': forms.TextInput(attrs={'class': 'form-control'}),
      'drc1': forms.TextInput(attrs={'class': 'form-control'}),
      'drc2': forms.TextInput(attrs={'class': 'form-control'}),
      'drc3': forms.TextInput(attrs={'class': 'form-control'}),
      'isc': forms.TextInput(attrs={'class': 'form-control'}), 
      'icc': forms.TextInput(attrs={'class': 'form-control'}), 
      'ire1': forms.TextInput(attrs={'class': 'form-control'}), 
      'ire2': forms.TextInput(attrs={'class': 'form-control'}),
      'ire3': forms.TextInput(attrs={'class': 'form-control'}),
      'iau': forms.TextInput(attrs={'class': 'form-control'}),
      'idc1': forms.Select(attrs={'class': 'form-control'}),
      'idc2': forms.TextInput(attrs={'class': 'form-control'}),
      'iph': forms.TextInput(attrs={'class': 'form-control'}),
      'ici': forms.TextInput(attrs={'class': 'form-control'}),
      'icl': forms.TextInput(attrs={'class': 'form-control'}),
      'irc1': forms.TextInput(attrs={'class': 'form-control'}),
      'irc2': forms.TextInput(attrs={'class': 'form-control'}),
      'irc3': forms.TextInput(attrs={'class': 'form-control'}),
      'adicion': forms.TextInput(attrs={'class': 'form-control'}),
      'tipo_lente': forms.TextInput(attrs={'class': 'form-control'}),
      'dto': forms.TextInput(attrs={'class': 'form-control'}),
      'ito': forms.TextInput(attrs={'class': 'form-control'}),
      'dbio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
      'ibio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
      'dfdo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
      'ifdo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
      'otros': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
    }

class DiagnosticoForm(forms.ModelForm):
  class Meta:
    model = Diagnostico
    fields = ('detalle', 'agenda')
    widgets = {
      'agenda': forms.HiddenInput(),
      'detalle': forms.TextInput(attrs={'class': 'form-control enviod'}),
    }

class TratamientoForm(forms.ModelForm):
  class Meta:
    model = Tratamiento
    fields = ('detalle', 'agenda')
    widgets = {
      'agenda': forms.HiddenInput(),
      'detalle': forms.TextInput(attrs={'class': 'form-control enviot'}),
    }

class AgendaservForm(forms.ModelForm):
  servicio = forms.ModelChoiceField(queryset=Servicio.objects.all(), empty_label="Seleccionar Servicio", widget=forms.Select(attrs={'class': 'form-control'}))
  class Meta:
    model = Agendaserv
    fields = ('servicio', 'costo', 'estado')
    widgets = {
      'costo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Costo'}),
      'estado': forms.CheckboxInput(attrs={'class': 'filled-in chk-col-blue'}),
    }

ServicioFormset = inlineformset_factory(Agenda, Agendaserv, AgendaservForm, can_delete=False, extra=1)