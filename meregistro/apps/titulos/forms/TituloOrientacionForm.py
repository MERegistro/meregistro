# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import TituloOrientacion, Titulo, EstadoTituloOrientacion


class TituloOrientacionForm(forms.ModelForm):
    titulo = forms.ModelChoiceField(queryset = Titulo.objects.order_by('nombre'), label = 'Título')
    observaciones = forms.CharField(widget = forms.Textarea, required = False)
    estado = forms.ModelChoiceField(queryset = EstadoTituloOrientacion.objects.all().order_by('nombre'), required = False, empty_label = None)

    class Meta:
        model = TituloOrientacion
