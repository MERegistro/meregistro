# -*- coding: UTF-8 -*-

from django import forms
from apps.validez_nacional.models import ValidezNacional
from apps.registro.models import Establecimiento
from apps.titulos.models import Cohorte

ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(Cohorte.PRIMER_ANIO, Cohorte.ULTIMO_ANIO)]
class ValidezInstitucionalFormFilters(forms.Form):
    cue = forms.CharField(max_length=11, label='CUE', required=False)
    carrera = forms.CharField(max_length=40, label='Carrera', required=False)
    titulo_nacional = forms.CharField(max_length=40, label='Título', required=False)
    primera_cohorte = forms.ChoiceField(label='Primera Cohorte', choices=ANIOS_COHORTE_CHOICES, required=False)
    normativas_nacionales = forms.CharField(max_length=40, label='Normativa Nacional', required=False)
    nro_infd = forms.CharField(max_length=40, label='Número INFD', required=False)

    def __init__(self, *args, **kwargs):
        self.establecimiento = kwargs.pop('establecimiento')
        super(ValidezInstitucionalFormFilters, self).__init__(*args, **kwargs)
        
        
    def buildQuery(self, q=None):
        from itertools import chain
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = ValidezNacional.objects.filter(tipo_unidad_educativa=ValidezNacional.TIPO_UE_SEDE, unidad_educativa_id=self.establecimiento.id) \
            | ValidezNacional.objects.filter(tipo_unidad_educativa=ValidezNacional.TIPO_UE_ANEXO,unidad_educativa_id__in=[a.id for a in self.establecimiento.anexos.all()])
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('cue'):
            q = q.filter(cue__icontains=self.cleaned_data['cue'])
        if filter_by('carrera'):
            q = q.filter(carrera__icontains=self.cleaned_data['carrera'])
        if filter_by('titulo_nacional'):
            q = q.filter(titulo_nacional__icontains=self.cleaned_data['titulo_nacional'])
        if filter_by('primera_cohorte'):
            q = q.filter(primera_cohorte=self.cleaned_data['primera_cohorte'])
        if filter_by('normativas_nacionales'):
            q = q.filter(normativas_nacionales__icontains=self.cleaned_data['normativas_nacionales'])
        if filter_by('nro_infd'):
            q = q.filter(nro_infd__icontains=self.cleaned_data['nro_infd'])
        return q
