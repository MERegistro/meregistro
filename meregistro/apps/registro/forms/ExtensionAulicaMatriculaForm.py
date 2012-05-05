# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
import datetime
from apps.registro.models import ExtensionAulicaMatricula

YEARS_CHOICES = [('', 'Seleccione...')] + [(int(n), str(n)) for n in range(1980, datetime.datetime.now().year + 1)]

class ExtensionAulicaMatriculaForm(forms.ModelForm):
    anio = forms.ChoiceField(choices=YEARS_CHOICES)
    
    class Meta:
        model = ExtensionAulicaMatricula
        exclude = ('extension_aulica',)
        
    def __init__(self, *args, **kwargs):
        self.extension_aulica = kwargs.pop('extension_aulica')
        super(ExtensionAulicaMatriculaForm, self).__init__(*args, **kwargs)


    def clean_anio(self):
        anio = self.cleaned_data['anio']
        try:
            matricula_existente = ExtensionAulicaMatricula.objects.get(extension_aulica=self.extension_aulica, anio=anio)
        except ExtensionAulicaMatricula.DoesNotExist:
            matricula_existente = None
        " Si ya hay una matrícula en ese año "
        if matricula_existente and matricula_existente != self.instance:
            msg = "La matrícula del año %s ya se ha definido." % (str(anio))
            raise ValidationError(msg)
        return anio
