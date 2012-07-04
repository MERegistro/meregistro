# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import Matricula
from apps.registro.models import Establecimiento
from django.db.models import Q

class MatriculaForm(forms.ModelForm):
    observaciones = forms.CharField(widget = forms.Textarea, required = False)
    establecimiento = forms.ModelChoiceField(queryset = Establecimiento.objects.order_by('nombre'), required = True, empty_label = None)
    class Meta:
        model = Matricula

    def clean(self):
        cleaned_data = self.cleaned_data
        q = Matricula.objects.filter(anio_lectivo=cleaned_data['anio_lectivo'])
        if cleaned_data['establecimiento'] is not None:
            q = q.filter(establecimiento = cleaned_data['establecimiento'])
        if cleaned_data['anexo'] is not None:
            q = q.filter(anexo = cleaned_data['anexo'])
        if self.instance is not None:
            q = q.exclude(pk=self.instance.id)
        if len(q) > 0:
            raise ValidationError(u'Ya está cargado el año ingresado.')
        return cleaned_data

