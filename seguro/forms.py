from django import forms
from .models import Seguro, Segurocosto
from servicio.models import Servicio

class SeguroForm(forms.ModelForm):
  class Meta:
    model = Seguro
    fields = ('nombre', 'direccion', 'telefono')

    widgets = {
      'nombre': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'telefono': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
      'direccion': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2}),
    }

class SegurocostoForm(forms.ModelForm):
  servicio = forms.ModelChoiceField(queryset=Servicio.objects.all(), empty_label=None,
                         widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
  class Meta:
    model = Segurocosto
    fields = ('seguro', 'servicio', 'costo')

    widgets = {
      'seguro': forms.HiddenInput(),
      'costo': forms.NumberInput(attrs={'class': 'form-control form-control-sm'})
    }