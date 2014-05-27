# -*- coding: UTF-8 -*-

from django import forms
from django.db.models import Max
from apps.postitulos.models import NormativaPostituloJurisdiccional, NormativaPostituloJurisdiccionalEstado, TipoNormativaPostituloJurisdiccional, NormativaPostituloMotivoOtorgamiento, EstadoNormativaPostituloJurisdiccional


class NormativaPostituloJurisdiccionalFormFilters(forms.Form):
    numero_anio = forms.CharField(label='Número/Año', required=False)
    tipo_normativa_postitulo_jurisdiccional = forms.ModelChoiceField(queryset = TipoNormativaPostituloJurisdiccional.objects.order_by('nombre'), label = 'Tipo de normativa', required = False)
    otorgada_por = forms.ModelChoiceField(queryset = NormativaPostituloMotivoOtorgamiento.objects.order_by('nombre'), label = 'Otorgada por', required = False)
    estado = forms.ModelChoiceField(queryset = EstadoNormativaPostituloJurisdiccional.objects.all().order_by('nombre'), required = False)


    def buildQuery(self, q = None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = NormativaPostituloJurisdiccional.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('tipo_normativa_postitulo_jurisdiccional'):
            q = q.filter(tipo_normativa_postitulo_jurisdiccional = self.cleaned_data['tipo_normativa_postitulo_jurisdiccional'])
        if filter_by('otorgada_por'):
            q = q.filter(otorgada_por = self.cleaned_data['otorgada_por'])
        if filter_by('estado'):
            q = q.filter(estado = self.cleaned_data['estado'])
        if filter_by('numero_anio'):
            q = q.filter(numero_anio__icontains = self.cleaned_data['numero_anio'])
        return q
