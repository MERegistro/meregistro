# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import TituloJurisdiccional, TituloJurisdiccionalCohorte, Carrera, \
    EstadoTituloJurisdiccional, TipoTitulo, CohorteEstablecimiento, EstadoCohorteEstablecimiento
import datetime

ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(2000, 2021)]

class AceptarCohorteEstablecimientoFormFilters(forms.Form):

    anio = forms.ChoiceField(label = 'Año', choices = ANIOS_COHORTE_CHOICES, required = False)
    tipo_titulo = forms.ModelChoiceField(queryset = TipoTitulo.objects.order_by('nombre'), label = 'Tipo de título', required = False)
    nombre_titulo = forms.CharField(max_length = 40, label = 'Nombre', required = False)
    carrera = forms.ModelChoiceField(queryset = Carrera.objects.all().order_by('nombre'), required = False)
    estado = forms.ModelChoiceField(queryset = EstadoCohorteEstablecimiento.objects.all().order_by('nombre'), required = False)

    def buildQuery(self, q = None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = CohorteEstablecimiento.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
            if filter_by('anio'):
                q = q.filter(cohorte__anio = self.cleaned_data['anio'])
            if filter_by('tipo_titulo'):
                q = q.filter(cohorte__titulo_jurisdiccional__titulo__tipo_titulo = self.cleaned_data['tipo_titulo'])
            if filter_by('nombre_titulo'):
                q = q.filter(cohorte__titulo_jurisdiccional__titulo__nombre__icontains = self.cleaned_data['nombre_titulo'])
            if filter_by('carrera'):
                q = q.filter(cohorte__titulo_jurisdiccional__titulo__carrera = self.cleaned_data['carrera'])
            if filter_by('estado'):
                q = q.filter(estado = self.cleaned_data['estado'])
        # Filtra que el año de la última cohorte sea menor o igual al año en curso y el estado sea controlado
        #q = q.filter()
        return q
