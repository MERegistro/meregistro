# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import TituloJurisdiccional, TituloJurisdiccionalCohorte, Carrera, EstadoTituloJurisdiccional, TipoTitulo
import datetime

class TituloJurisdiccionalCohorteFormFilters(forms.Form):

    tipo_titulo = forms.ModelChoiceField(queryset = TipoTitulo.objects.order_by('nombre'), label = 'Tipo de título', required = False)
    nombre_titulo = forms.CharField(max_length = 40, label = 'Nombre', required = False)
    carrera = forms.ModelChoiceField(queryset = Carrera.objects.all().order_by('nombre'), required = False)

    def buildQuery(self, q = None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = TituloJurisdiccional.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('tipo_titulo'):
            q = q.filter(tipo_titulo = self.cleaned_data['tipo_titulo'])
        if filter_by('nombre_titulo'):
            q = q.filter(titulo__nombre__icontains = self.cleaned_data['nombre_titulo'])
        if filter_by('carrera'):
            q = q.filter(titulo__carrera = self.cleaned_data['carrera'])
        # Filtra que el año de la última cohorte sea menor o igual al año en curso y el estado sea controlado
        q = q.filter(estado__nombre = EstadoTituloJurisdiccional.CONTROLADO, datos_cohorte__anio_ultima_cohorte__gte = datetime.date.today().year)
        return q
