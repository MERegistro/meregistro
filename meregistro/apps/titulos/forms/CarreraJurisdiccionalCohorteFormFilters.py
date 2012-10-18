# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import CarreraJurisdiccional, CarreraJurisdiccionalCohorte, Carrera, EstadoCarreraJurisdiccional, TipoTitulo
import datetime

ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(1970, 2021)]
    
class CarreraJurisdiccionalCohorteFormFilters(forms.Form):

    tipo_titulo = forms.ModelChoiceField(queryset = TipoTitulo.objects.order_by('nombre'), label = 'Tipo de título', required = False)
    nombre_titulo = forms.CharField(max_length = 40, label = 'Nombre', required = False)
    carrera = forms.ModelChoiceField(queryset = Carrera.objects.all().order_by('nombre'), required = False)
    anio_primera_cohorte = forms.ChoiceField(label = 'Año primera cohorte', choices = ANIOS_COHORTE_CHOICES, required = False)
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
            if filter_by('tipo_titulo'):
                q = q.filter(titulo__tipo_titulo = self.cleaned_data['tipo_titulo'])
            if filter_by('nombre_titulo'):
                q = q.filter(titulo__nombre__icontains = self.cleaned_data['nombre_titulo'])
            if filter_by('carrera'):
                q = q.filter(titulo__carrera = self.cleaned_data['carrera'])
            if filter_by('anio_primera_cohorte'):
                #q = q.filter(datos_cohorte__anio_primera_cohorte = self.cleaned_data['anio_primera_cohorte'])
				pass
            if filter_by('estado'):
                q = q.filter(estado = self.cleaned_data['estado'])
        # Filtra que el año de la última cohorte sea menor o igual al año en curso y el estado sea controlado -> CANCELADO
        #q = q.order_by('datos_cohorte__anio_primera_cohorte', 'titulo__nombre')
        q = q.order_by('datos_cohorte__primera_cohorte_solicitada', 'carrera__nombre')
        return q
