# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import Matricula

class MatriculaFormFilters(forms.Form):
    cue = forms.CharField(max_length = 40, label = 'Cue', required = False)


    def buildQuery(self, q = None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = Matricula.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
            if filter_by('cue'):
                cue_establecimiento = self.cleaned_data['cue']
                if len(self.cleaned_data['cue']) > 5:
                    cue_establecimiento = self.cleaned_data['cue'][:5]
                    q = q.filter(anexo__cue__istartswith=self.cleaned_data['cue'][5:])
                q = q.filter(establecimiento__cue__istartswith = cue_establecimiento)
        return q
