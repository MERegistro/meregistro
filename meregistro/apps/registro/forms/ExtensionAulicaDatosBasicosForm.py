# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.Turno import Turno
from apps.registro.forms.ExtensionAulicaCreateForm import ExtensionAulicaCreateForm
from django.core.exceptions import ValidationError
from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime


currentYear = datetime.datetime.now().year

class ExtensionAulicaDatosBasicosForm(ExtensionAulicaCreateForm):
    posee_centro_estudiantes = forms.ChoiceField(choices=((None, ''), (False, 'No'), (True, 'Sí')), required=False)
    posee_representantes_estudiantiles = forms.ChoiceField(choices=((None, ''), (False, 'No'), (True, 'Sí')), required=False)

    class Meta:
        model = ExtensionAulica
        exclude = ('establecimiento', 'estado', 'funciones', 'alcances', 'turnos', 'sitio_web', 'telefono', 'email', 'normativa', 'tipo_normativa')

    def __init__(self, *args, **kwargs):
        super(ExtensionAulicaDatosBasicosForm, self).__init__(*args, **kwargs)
        self.fields['codigo_jurisdiccion'].required = False
        self.fields['cue'].required = False
        self.fields['codigo_tipo_unidad_educativa'].required = False


    def clean_codigo_tipo_unidad_educativa(self):
        return self.instance.get_cue_parts()['codigo_tipo_unidad_educativa']

    def clean_codigo_jurisdiccion(self):
        return self.instance.get_cue_parts()['codigo_jurisdiccion']

    def clean_cue(self):
        return self.instance.get_cue_parts()['cue']
        
    def clean_subsidio(self):
        from apps.registro.models import TipoSubsidio, TipoGestion
        subsidio = self.cleaned_data['subsidio']
        establecimiento = self.instance.establecimiento
        tipo_gestion = establecimiento.dependencia_funcional.tipo_gestion.nombre
        if tipo_gestion == TipoGestion.ESTATAL and subsidio.descripcion != TipoSubsidio.SIN_SUBSIDIO:
            raise ValidationError('La Extensión Áulica no puede poseer subsidio ya que depende de una sede estatal')
        return subsidio
