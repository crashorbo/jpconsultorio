from django import forms
from .models import Seguro

class SeguroForm(forms.ModelForm):
  class Meta:
    model = Seguro
    fields = ('nombre', 'direccion', 'telefono')

    widgets = {
      'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
      'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono'}),
      'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Direccion'}),
    }