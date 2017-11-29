# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import Establecimiento
from apps.seguridad.models import TipoDocumento
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoContactoForm(ModelForm):
    verificado = forms.BooleanField(required=False)
    director_tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects.order_by('descripcion'), label='Tipo de documento', required=False)
    director_fecha_nacimiento = forms.DateField(
        input_formats=['%d/%m/%Y', '%d/%m/%y'],
        required=False,
        widget=forms.DateInput(attrs={'class':'datePicker'}))

    class Meta:
        model = Establecimiento
        fields = ['telefono', 'interno', 'fax', 'sitio_web', 'email', \
            'director_apellido', 'director_nombre', 'director_fecha_nacimiento', \
            'director_tipo_documento', 'director_documento', 'director_telefono', 'director_celular', 'director_email']

    def clean(self):
        telefono = self.cleaned_data['telefono']
        interno = self.cleaned_data['interno']
        if interno and telefono == '':
            raise ValidationError('Por favor ingrese el número de teléfono')
            
        return self.cleaned_data



    
