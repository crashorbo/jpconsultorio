from django import forms

from .models import Reportegeneral


class ReportegeneralForm(forms.ModelForm):
    class Meta:
        model = Reportegeneral
        fields = ('mes', 'gestion')

        widgets = {
            'mes': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'gestion': forms.HiddenInput(),
        }
