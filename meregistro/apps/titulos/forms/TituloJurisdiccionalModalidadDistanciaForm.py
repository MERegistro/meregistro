# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import TituloJurisdiccionalModalidadDistancia

DURACION_CHOICES = [('', '-------')] + [(i, i) for i in range(1, 6)]
CUATRIMESTRES_CHOICES = [('', '-------')] + [(i, i) for i in range(1, 3)]


class TituloJurisdiccionalModalidadDistanciaForm(forms.ModelForm):
    posee_mod_distancia = forms.BooleanField(required = False)
    duracion = forms.ChoiceField(label = 'Duración', choices = DURACION_CHOICES, required = False)
    cuatrimestres = forms.ChoiceField(label = 'Cuatrimestres', choices = CUATRIMESTRES_CHOICES, required = False)
    nro_dictamen = forms.CharField(label = 'Nro. dictámen', required = False)

    
    class Meta:
        model = TituloJurisdiccionalModalidadDistancia
        exclude = ('titulo',)

    def clean(self):
        cleaned_data = self.cleaned_data
        # Modalidad distancia
        posee_mod_distancia = cleaned_data['posee_mod_distancia']
        if not posee_mod_distancia: # Los reseteo, pero en la vista los elimino
            cleaned_data['duracion'] = None
            cleaned_data['cuatrimestres'] = None
        elif str(cleaned_data['duracion']) == '':
            raise ValidationError('Debe elegir la duración.')
        elif str(cleaned_data['cuatrimestres']) == '':
            cleaned_data['cuatrimestres'] = None # sino arroja: "invalid literal for int() with base 10: ''"
        return cleaned_data
