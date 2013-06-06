# -*- coding: UTF-8 -*-

from django import forms
from apps.validez_nacional.models import Solicitud, EstadoSolicitud
from apps.titulos.models import Cohorte
from django.db.models import Min, Max

primera_cohorte = Solicitud.objects.all().aggregate(Min('primera_cohorte'))['primera_cohorte__min']
ultima_cohorte = Solicitud.objects.all().aggregate(Max('primera_cohorte'))['primera_cohorte__max']
if primera_cohorte is None:
	primera_cohorte = Cohorte.PRIMER_ANIO
if ultima_cohorte is None:
	ultima_cohorte = Cohorte.ULTIMO_ANIO
	
ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(primera_cohorte, ultima_cohorte+1)]

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
