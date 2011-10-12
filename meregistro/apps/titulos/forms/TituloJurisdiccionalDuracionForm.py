# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from apps.titulos.models import TituloJurisdiccional

HORAS_DURACION_4 = 2600
HORAS_DURACION_5 = 2860

class TituloJurisdiccionalDuracionForm(forms.ModelForm):
    horas_reloj = forms.IntegerField(label = 'Horas reloj', required = False)

    class Meta:
        model = TituloJurisdiccional
        fields = ('horas_reloj',)
        
    "Le agrego datos para chequear"
    def __init__(self, *args, **kwargs):
        self.duracion_mod_distancia = kwargs.pop('duracion_mod_distancia')
        self.duracion_mod_presencial = kwargs.pop('duracion_mod_presencial')
        super(TituloJurisdiccionalDuracionForm, self).__init__(*args, **kwargs)

        
    """
    Si duración es 4, las horas reloj deeben ser al menos 2600
    Si duración es 5, las horas reloj deeben ser al menos 2860
    """
    
    def clean_horas_reloj(self):
        if self.duracion_mod_distancia is not None:
            duracion = self.duracion_mod_distancia
        else:
            duracion = self.duracion_mod_presencial

        try:
            horas_reloj = int(self.cleaned_data['horas_reloj'])
        except:
            horas_reloj = None

        if duracion is not None:
            try:
                duracion = int(duracion)            
            except ValueError:
                pass
        
        if duracion is 4 and (horas_reloj < HORAS_DURACION_4 or horas_reloj is None):            
            raise ValidationError(u'La duración elegida requiere al menos ' + str(HORAS_DURACION_4) + ' horas reloj.')
        elif duracion is 5 and (horas_reloj < HORAS_DURACION_5 or horas_reloj is None):
            raise ValidationError(u'La duración elegida requiere al menos ' + str(HORAS_DURACION_5) + ' horas reloj.')
        return self.cleaned_data['horas_reloj']
    
