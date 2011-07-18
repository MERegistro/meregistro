# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import NormativaJurisdiccional, TipoNormativaJurisdiccional, NormativaMotivoOtorgamiento, EstadoNormativaJurisdiccional


class NormativaJurisdiccionalFormFilters(forms.Form):
    tipo_normativa_jurisdiccional = forms.ModelChoiceField(queryset = TipoNormativaJurisdiccional.objects.order_by('nombre'), label = 'Tipo de normativa', required = False)
    otorgada_por = forms.ModelChoiceField(queryset = NormativaMotivoOtorgamiento.objects.order_by('nombre'), label = 'Otorgada por', required = False)
    estado = forms.ModelChoiceField(queryset = EstadoNormativaJurisdiccional.objects.all().order_by('nombre'), required = False)

    def buildQuery(self, q = None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = NormativaJurisdiccional.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('tipo_normativa_jurisdiccional'):
            q = q.filter(tipo_normativa_jurisdiccional = self.cleaned_data['tipo_normativa_jurisdiccional'])
        if filter_by('otorgada_por'):
            q = q.filter(otorgada_por = self.cleaned_data['otorgada_por'])
        if filter_by('estado'):
            q = q.filter(estado = self.cleaned_data['estado'])
        return q
