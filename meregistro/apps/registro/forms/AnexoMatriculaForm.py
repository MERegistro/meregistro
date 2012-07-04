# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
import datetime
from apps.registro.models import AnexoMatricula

YEARS_CHOICES = [('', 'Seleccione...')] + [(int(n), str(n)) for n in range(1980, datetime.datetime.now().year + 1)]

class AnexoMatriculaForm(forms.ModelForm):
    anio = forms.ChoiceField(choices=YEARS_CHOICES)
    
    class Meta:
        model = AnexoMatricula
        exclude = ('anexo',)
        
    def __init__(self, *args, **kwargs):
        self.anexo = kwargs.pop('anexo')
        super(AnexoMatriculaForm, self).__init__(*args, **kwargs)


    def clean_anio(self):
        anio = self.cleaned_data['anio']
        try:
            matricula_existente = AnexoMatricula.objects.get(anexo=self.anexo, anio=anio)
        except AnexoMatricula.DoesNotExist:
            matricula_existente = None
        " Si ya hay una matrícula en ese año "
        if matricula_existente and matricula_existente != self.instance:
            msg = "La matrícula del año %s ya se ha definido." % (str(anio))
            raise ValidationError(msg)
        return anio
