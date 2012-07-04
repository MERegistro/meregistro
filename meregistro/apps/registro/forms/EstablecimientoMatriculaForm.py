# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
import datetime
from apps.registro.models import EstablecimientoMatricula

YEARS_CHOICES = [('', 'Seleccione...')] + [(int(n), str(n)) for n in range(1980, datetime.datetime.now().year + 1)]

class EstablecimientoMatriculaForm(forms.ModelForm):
    anio = forms.ChoiceField(choices=YEARS_CHOICES)
    
    class Meta:
        model = EstablecimientoMatricula
        exclude = ('establecimiento',)
        
    def __init__(self, *args, **kwargs):
        self.establecimiento = kwargs.pop('establecimiento')
        super(EstablecimientoMatriculaForm, self).__init__(*args, **kwargs)



    def clean_anio(self):
        anio = self.cleaned_data['anio']
        try:
            matricula_existente = EstablecimientoMatricula.objects.get(establecimiento=self.establecimiento, anio=anio)
        except EstablecimientoMatricula.DoesNotExist:
            matricula_existente = None
        " Si ya hay una matrícula en ese año "
        if matricula_existente and matricula_existente != self.instance:
            msg = "La matrícula del año %s ya se ha definido." % (str(anio))
            raise ValidationError(msg)
        return anio
