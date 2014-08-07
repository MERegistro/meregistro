# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.Anexo import Anexo
from apps.registro.models.Turno import Turno
from apps.registro.forms.AnexoCreateForm import AnexoCreateForm
from django.core.exceptions import ValidationError
from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime


currentYear = datetime.datetime.now().year

class AnexoDatosBasicosForm(AnexoCreateForm):    
    
    class Meta:
        model = Anexo
        exclude = ('codigo_tipo_unidad_educativa', 'establecimiento', 'estado', 'funciones', 'alcances', 'turnos', 'sitio_web', 'telefono', 'email',)


    def __init__(self, *args, **kwargs):
        super(AnexoDatosBasicosForm, self).__init__(*args, **kwargs)
        self.fields['codigo_jurisdiccion'].required = False
        self.fields['cue'].required = False
        self.fields['codigo_tipo_unidad_educativa'].required = False

    def clean_codigo_tipo_unidad_educativa(self):
        return


    def clean_subsidio(self):
        return self.instance.subsidio
