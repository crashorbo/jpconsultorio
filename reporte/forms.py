from django import forms

from .models import Reportegeneral, Reporteseguro


class ReportegeneralForm(forms.ModelForm):
    class Meta:
        model = Reportegeneral
        fields = ('mes', 'gestion')

        widgets = {
            'mes': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'gestion': forms.HiddenInput(),
        }


class ReporteseguroForm(forms.ModelForm):
    class Meta:
        model = Reporteseguro
        fields = ('mes', 'seguro', 'gestion')

        widgets = {
            'mes': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'gestion': forms.HiddenInput(),
            'seguro': forms.HiddenInput(),
        }
