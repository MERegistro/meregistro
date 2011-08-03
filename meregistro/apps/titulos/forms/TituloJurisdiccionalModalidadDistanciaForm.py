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
    horas_reloj = forms.IntegerField(label = 'Horas reloj', required = False)

    class Meta:
        model = TituloJurisdiccionalModalidadDistancia
        exclude = ('titulo',)

    def clean(self):
        cleaned_data = self.cleaned_data
        # Modalidad distancia
        posee_mod_distancia = cleaned_data['posee_mod_distancia']
        if not posee_mod_distancia:
            cleaned_data['duracion'] = 1
        elif str(cleaned_data['duracion']) == '':
            raise ValidationError('Debe elegir la duración.')
        elif str(cleaned_data['cuatrimestres']) == '':
            raise ValidationError('Debe elegir la cantidad de cuatrimestres.')
        return cleaned_data

    """
    Si duración es 4, las horas reloj deeben ser al menos 2600
    Si duración es 5, las horas reloj deeben ser al menos 2860
    """
    def clean_horas_reloj(self):
        try:
            duracion = int(self.cleaned_data['duracion'])
        except:
            duracion = None
        try:
            horas_reloj = int(self.cleaned_data['horas_reloj'])
        except:
            horas_reloj = None

        if duracion is 4 and (horas_reloj < 2600 or horas_reloj is None):
            raise ValidationError(u'La duración elegida requiere al menos 2600 horas reloj.')
        elif duracion is 5 and (horas_reloj < 2800 or horas_reloj is None):
            raise ValidationError(u'La duración elegida requiere al menos 2860 horas reloj.')
        return self.cleaned_data['horas_reloj']
