# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import Postitulo

class PostituloForm(forms.ModelForm):
#    observaciones = forms.CharField(widget = forms.Textarea, required = False)

    class Meta:
        model = Postitulo
