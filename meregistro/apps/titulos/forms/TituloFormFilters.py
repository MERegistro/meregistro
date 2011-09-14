# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import Jurisdiccion
from apps.titulos.models import Titulo, EstadoTitulo, TipoTitulo


class TituloFormFilters(forms.Form):

    TIENE_ORIENTACIONES_CHOICES = (
        ('', '---------'),
        ('1', ' Sí'),
        ('0', 'No'),
    )

    nombre = forms.CharField(max_length = 40, label = 'Nombre', required = False)
    tipo_titulo = forms.ModelChoiceField(queryset = TipoTitulo.objects.order_by('nombre'), label = 'Tipo de título', required = False)
    jurisdiccion = forms.ModelChoiceField(queryset = Jurisdiccion.objects.order_by('nombre'), label = 'Jurisdicción', required = False)
    estado = forms.ModelChoiceField(queryset = EstadoTitulo.objects.all().order_by('nombre'), required = False)
    tiene_orientaciones = forms.ChoiceField(label = 'Con orientaciones', required = False, choices = TIENE_ORIENTACIONES_CHOICES)

    def buildQuery(self, q = None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = Titulo.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('tipo_titulo'):
            q = q.filter(tipo_titulo = self.cleaned_data['tipo_titulo'])
        if filter_by('nombre'):
            q = q.filter(nombre__icontains = self.cleaned_data['nombre'])
        if filter_by('jurisdiccion'):
            q = q.filter(jurisdicciones__id = self.cleaned_data['jurisdiccion'].id)
        if filter_by('tiene_orientaciones'):
            q = q.filter(tiene_orientaciones = self.cleaned_data['tiene_orientaciones'])
        if filter_by('estado'):
            q = q.filter(estado = self.cleaned_data['estado'])
        return q
