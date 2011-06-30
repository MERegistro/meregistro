# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import DependenciaFuncional


class DependenciaFuncionalForm(ModelForm):

    class Meta:
        model = DependenciaFuncional
