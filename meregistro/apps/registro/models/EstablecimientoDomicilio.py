# -*- coding: utf-8 -*-
from django.db import models
from meregistro.apps.registro.models.TipoDomicilio import TipoDomicilio
from meregistro.apps.registro.models.Localidad import Localidad
from meregistro.apps.registro.models.Establecimiento import Establecimiento
from django.core.exceptions import ValidationError


class EstablecimientoDomicilio(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, related_name='domicilio')
    tipo_domicilio = models.ForeignKey(TipoDomicilio)
    localidad = models.ForeignKey(Localidad, related_name='domicilios_establecimientos')
    calle = models.CharField(max_length=100)
    altura = models.CharField(max_length=5)
    referencia = models.CharField(max_length=255, null=True, blank=True)
    cp = models.CharField(max_length=20)

    class Meta:
        app_label = 'registro'
        db_table = 'registro_establecimiento_domicilio'

    def __unicode__(self):
        if self.cp:
            cp = " (CP: " + self.cp + ")"
        else:
            cp = ""
        return str(self.calle) + " " + str(self.altura) + " - " + self.localidad.nombre + cp

    def __init__(self, *args, **kwargs):
        super(EstablecimientoDomicilio, self).__init__(*args, **kwargs)
