# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.postitulos .models import InformeSolicitud


class InformeSolicitudForm(forms.ModelForm):
    observaciones = forms.CharField(max_length=999, required=False, widget=forms.Textarea(attrs={'rows': '10', 'cols': '100'}))
    
    class Meta:
       model = InformeSolicitud
       exclude = ('solicitud',)
