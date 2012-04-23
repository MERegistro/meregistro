# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.registro.models import ExtensionAulicaMatricula


class ExtensionAulicaMatriculaForm(forms.ModelForm):
    
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
