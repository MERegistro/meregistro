# -*- coding: UTF-8 -*-

from django import forms
from seguridad.models import TipoDocumento, Usuario


class UsuarioFormFilters(forms.Form):
    tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects, required=False)
    documento = forms.CharField(max_length=20, label='documento', required=False)
    apellido = forms.CharField(max_length=40, label='apellido', required=False)
    nombre = forms.CharField(max_length=40, label='nombre', required=False)
    email = forms.CharField(max_length=255, label='email', required=False)

    def buildQuery(self, q=None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = Usuario.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
            if filter_by('documento'):
                q = q.filter(documento__istartswith=self.cleaned_data['documento'])
            if filter_by('nombre'):
                q = q.filter(nombre__istartswith=self.cleaned_data['nombre'])
            if filter_by('apellido'):
                q = q.filter(apellido__istartswith=self.cleaned_data['apellido'])
            if filter_by('email'):
                q = q.filter(email__istartswith=self.cleaned_data['email'])
            if filter_by('tipo_documento'):
                q = q.filter(tipo_documento=self.cleaned_data['tipo_documento'])
        return q
