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
      'antocu': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'tabindex': 1, 'rows': 2}),
      'antsis': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'tabindex': 2, 'rows': 2}),
      'motivo': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'tabindex': 3, 'rows': 2}),
      'dsc': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 4}), 
      'dcc': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 5}), 
      'dre1': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 6}), 
      'dre2': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 7}),
      'dre3': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 8}),
      'dau': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 9}),
      'ddc1': forms.Select(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 10}),
      'ddc2': forms.TextInput(attrs={'class': 'form-control form-control-sm  text-center', 'tabindex': 11}),
      'dph': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 12}),
      'dci': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 13}),
      'dcl': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 14}),
      'drc1': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 15}),
      'drc2': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 16}),
      'drc3': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 17}),
      'isc': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 18}), 
      'icc': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 19}), 
      'ire1': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 20}), 
      'ire2': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 21}),
      'ire3': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 22}),
      'iau': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 23}),
      'idc1': forms.Select(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 24}),
      'idc2': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 25}),
      'iph': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 26}),
      'ici': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 27}),
      'icl': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 28}),
      'irc1': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 29}),
      'irc2': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 30}),
      'irc3': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 31}),
      'adicion': forms.TextInput(attrs={'class': 'form-control form-control-sm text-center', 'tabindex': 32}),
      'tipo_lente': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'tabindex': 33}),
      'dto': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'tabindex': 34}),
      'ito': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'tabindex': 35}),
      'dbio': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3, 'tabindex': 36}),
      'ibio': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3, 'tabindex': 37}),
      'dfdo': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3, 'tabindex': 38}),
      'ifdo': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3, 'tabindex': 39}),
      'otros': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2, 'tabindex': 40}),
    }

class DiagnosticoForm(forms.ModelForm):
  class Meta:
    model = Diagnostico
    fields = ('detalle', 'agenda')
    widgets = {
      'agenda': forms.HiddenInput(),
      'detalle': forms.TextInput(attrs={'class': 'form-control form-control-sm enviod', 'tabindex': 41}),
    }

class TratamientoForm(forms.ModelForm):
  class Meta:
    model = Tratamiento
    fields = ('detalle', 'agenda')
    widgets = {
      'agenda': forms.HiddenInput(),
      'detalle': forms.TextInput(attrs={'class': 'form-control form-control-sm enviot', 'tabindex': 42}),
    }

class AgendaservForm(forms.ModelForm):
  servicio = forms.ModelChoiceField(queryset=Servicio.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
  class Meta:
    model = Agendaserv
    fields = ('servicio', 'costo', 'estado')
    widgets = {
      'costo': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Costo'}),
      'estado': forms.CheckboxInput(attrs={'class': 'filled-in chk-col-blue form-control-sm'}),
    }

ServicioFormset = inlineformset_factory(Agenda, Agendaserv, AgendaservForm, can_delete=False, extra=1)