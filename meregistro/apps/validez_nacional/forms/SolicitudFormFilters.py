# -*- coding: UTF-8 -*-

from django import forms
from apps.validez_nacional.models import Solicitud, EstadoSolicitud
from apps.titulos.models import Cohorte

ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(Cohorte.PRIMER_ANIO, Cohorte.ULTIMO_ANIO)]

class SolicitudFormFilters(forms.Form):

    titulo = forms.CharField(max_length=40, label='Título', required=False)
    primera_cohorte = forms.ChoiceField(label='Cohorte', choices=ANIOS_COHORTE_CHOICES, required=False)
    estado = forms.ModelChoiceField(queryset=EstadoSolicitud.objects.all().order_by('nombre'), required=False)

    def buildQuery(self, q=None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = Solicitud.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('titulo'):
            q = q.filter(titulo_nacional__nombre__icontains=self.cleaned_data['titulo'])
        if filter_by('primera_cohorte'):
            q = q.filter(primera_cohorte=self.cleaned_data['primera_cohorte'])
        if filter_by('estado'):
            q = q.filter(estado=self.cleaned_data['estado'])
        return q
