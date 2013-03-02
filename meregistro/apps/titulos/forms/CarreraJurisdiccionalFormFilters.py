# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import CarreraJurisdiccional, Carrera, EstadoCarreraJurisdiccional, TipoTitulo, Cohorte	
import datetime

ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(Cohorte.PRIMER_ANIO, Cohorte.ULTIMO_ANIO)]
	

class CarreraJurisdiccionalFormFilters(forms.Form):

    cohorte = forms.ChoiceField(label='Cohorte', choices=ANIOS_COHORTE_CHOICES, required=False)
    carrera = forms.CharField(required = False)
    estado = forms.ModelChoiceField(queryset = EstadoCarreraJurisdiccional.objects.all().order_by('nombre'), required = False)

    def buildQuery(self, q = None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = CarreraJurisdiccional.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('cohorte'):
            pass #q = q.filter(titulo__tipo_titulo = self.cleaned_data['tipo_titulo'])
        if filter_by('estado'):
            q = q.filter(estado = self.cleaned_data['estado'])
        if filter_by('carrera'):
            q = q.filter(carrera__nombre__icontains = self.cleaned_data['carrera'])
        return q
