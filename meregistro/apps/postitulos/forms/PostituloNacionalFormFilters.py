# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import TituloNacional, EstadoTituloNacional, NormativaNacional, EstadoNormativaNacional


class PostituloNacionalFormFilters(forms.Form):

    nombre = forms.CharField(max_length=40, label='Nombre', required=False)
    normativa_nacional = forms.ModelChoiceField(queryset=NormativaNacional.objects.filter(estado__nombre=EstadoNormativaNacional.VIGENTE).order_by('numero'), label='Normativa', required=False)
    estado = forms.ModelChoiceField(queryset=EstadoTituloNacional.objects.all().order_by('nombre'), required=False)

    def buildQuery(self, q = None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = TituloNacional.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('nombre'):
            q = q.filter(nombre__icontains=self.cleaned_data['nombre'])
        if filter_by('normativa_nacional'):
            q = q.filter(normativa_nacional=self.cleaned_data['normativa_nacional'])
        if filter_by('estado'):
            q = q.filter(estado = self.cleaned_data['estado'])
        # 394
        #return q.filter(normativa_nacional__estado__nombre=EstadoNormativaNacional.VIGENTE)
        return q
