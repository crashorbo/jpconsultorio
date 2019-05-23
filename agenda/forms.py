from django import forms
from django.forms.models import inlineformset_factory
from .models import Agenda, Diagnostico, Tratamiento, Agendaserv
from dal import autocomplete
from paciente.models import Paciente
from seguro.models import Seguro
from servicio.models import Servicio

class AgendaForm(forms.ModelForm):
  paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), empty_label="Seleccionar Paciente", widget=autocomplete.ModelSelect2(url='paciente-autocomplete', attrs={'class': 'form-control form-control-sm'}))
  seguro = forms.ModelChoiceField(queryset=Seguro.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
  
  class Meta:
    model = Agenda
    fields = ('paciente', 'seguro', 'fecha', 'hora_inicio', 'hora_fin', 'tipo', 'prioridad', 'procedencia', 'matricula', 'tipo_beneficiario', 'antocu', 'antsis', 'motivo', 'dsc', 'dcc', 'dre1', 'dre2', 'dre3', 'dau', 'ddc1', 'ddc2', 'dph', 'dci', 'dcl', 'drc1', 'drc2', 'drc3', 'isc', 'icc', 'ire1', 'ire2', 'ire3', 'iau', 'idc1', 'idc2', 'iph', 'ici', 'icl', 'irc1', 'irc2', 'irc3', 'adicion', 'tipo_lente', 'dto', 'ito', 'dbio', 'ibio', 'dfdo', 'ifdo', 'otros')

    widgets = {
      'fecha': forms.DateInput(attrs={'class': 'form-control fecha form-control-sm'}),
      'hora_inicio': forms.TimeInput(format='%H:%M', attrs={'class': 'form-control form-control-sm clockpicker','data-placement':'bottom', 'data-align':'top', 'data-autoclose':'true'}),
      'hora_fin': forms.TimeInput(format='%H:%M', attrs={'class': 'form-control form-control-sm clockpicker','data-placement':'bottom', 'data-align':'top', 'data-autoclose':'true'}),
      'tipo': forms.Select(attrs={'class': 'form-control form-control-sm'}),
      'prioridad': forms.Select(attrs={'class': 'form-control form-control-sm'}),
      'procedencia': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'matricula': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Matricula'}),
      'tipo_beneficiario': forms.Select(attrs={'class': 'form-control form-control-sm'}),
      'antocu': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2}),
      'antsis': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2}),
      'motivo': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2}),
      'dsc': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}), 
      'dcc': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}), 
      'dre1': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}), 
      'dre2': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'dre3': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'dau': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'ddc1': forms.Select(attrs={'class': 'form-control form-control-sm text-center'}),
      'ddc2': forms.TextInput(attrs={'class': 'form-control form-control-sm  text-center'}),
      'dph': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'dci': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'dcl': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'drc1': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'drc2': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'drc3': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'isc': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}), 
      'icc': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}), 
      'ire1': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}), 
      'ire2': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'ire3': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'iau': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'idc1': forms.Select(attrs={'class': 'form-control form-control-sm text-center'}),
      'idc2': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'iph': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'ici': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'icl': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'irc1': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'irc2': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'irc3': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'adicion': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center'}),
      'tipo_lente': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'dto': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'ito': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'dbio': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
      'ibio': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
      'dfdo': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
      'ifdo': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
      'otros': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2}),
    }

class DiagnosticoForm(forms.ModelForm):
  class Meta:
    model = Diagnostico
    fields = ('detalle', 'agenda')
    widgets = {
      'agenda': forms.HiddenInput(),
      'detalle': forms.TextInput(attrs={'class': 'form-control form-control-sm enviod'}),
    }

class TratamientoForm(forms.ModelForm):
  class Meta:
    model = Tratamiento
    fields = ('detalle', 'agenda')
    widgets = {
      'agenda': forms.HiddenInput(),
      'detalle': forms.TextInput(attrs={'class': 'form-control form-control-sm enviot'}),
    }

class AgendaservForm(forms.ModelForm):
  servicio = forms.ModelChoiceField(queryset=Servicio.objects.all(), empty_label="Seleccionar Servicio", widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
  class Meta:
    model = Agendaserv
    fields = ('servicio', 'costo', 'estado')
    widgets = {
      'costo': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Costo'}),
      'estado': forms.CheckboxInput(attrs={'class': 'filled-in chk-col-blue form-control-sm'}),
    }

ServicioFormset = inlineformset_factory(Agenda, Agendaserv, AgendaservForm, can_delete=False, extra=1)