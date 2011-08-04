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

    def clean_horas_reloj(self):
        return self.cleaned_data['horas_reloj']

    """
    * Si "posee" es True, "duracion" es requerido
    * Si "duracion" es 4, horas_reloj es...no sé...

    def clean(self):
        pass
    """
"""
---------------------------------
* A Distancia (check)

Evento del sistema: Si selecciona esta opción el sistema solicita los siguientes datos:

 * Años de duración de la carrera: ( Numérico >0 >= 4, requerido)
 * Cuatrimestres: ( Numérico =>0 <= 2, no requerido)
 * Número de dictamen: (texto 50)

Horas reloj:  Si Años de duración de la carrera es 4 ( Numérico >0 >= 2600) o Años de duración de la carrera es 5 ( Numérico >0 >= 2860); requerido

"""
