# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import CohorteEstablecimiento, CohorteEstablecimientoSeguimiento


class CohorteEstablecimientoSeguimientoForm(forms.ModelForm):
    anio = forms.ChoiceField(label = 'Año', required = True)
    observaciones = forms.CharField(widget = forms.Textarea, required = False)

    class Meta:
        model = CohorteEstablecimientoSeguimiento

    "Le agrego el inscriptos_total para chequear la suma"
    def __init__(self, *args, **kwargs):
        self.inscriptos_total = kwargs.pop('inscriptos_total')
        self.anio_cohorte =  kwargs.pop('anio_cohorte')
        self.cohorte_establecimiento_id =  kwargs.pop('cohorte_establecimiento_id')
        super(CohorteEstablecimientoSeguimientoForm, self).__init__(*args, **kwargs)
        self.fields["anio"].choices = [('', '-------')] + [(i, i) for i in range(int(self.anio_cohorte) + 1, 2051)]
        self.fields["cohorte_establecimiento"].initial = self.cohorte_establecimiento_id

    def clean(self):
        try:
            solo_cursan_nueva = int(self.cleaned_data['solo_cursan_nueva'])
            no_cursan = int(self.cleaned_data['no_cursan'])
            recursan_cursan = int(self.cleaned_data['recursan_cursan'])
            solo_recursan = int(self.cleaned_data['solo_recursan'])
            if solo_cursan_nueva + no_cursan + recursan_cursan + solo_recursan != self.inscriptos_total:
                raise ValidationError('La suma de las cantidades dadas deben sumar ' + str(self.inscriptos_total) + ', el total de inscriptos en la cohorte.')
        except KeyError:
            pass
        return self.cleaned_data

    def clean_anio(self):
        cohorte_establecimiento_id = self.cleaned_data['cohorte_establecimiento'].id
        try:
            registro = CohorteEstablecimientoSeguimiento.objects.get(cohorte_establecimiento = cohorte_establecimiento_id, anio = self.cleaned_data['anio'])
        except:
            registro = None
        if registro is not None and registro.id != self.instance.id:
            raise ValidationError("Ya se realiza el seguimiento para este año")
        return self.cleaned_data['anio']
