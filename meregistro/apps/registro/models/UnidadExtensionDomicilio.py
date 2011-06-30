# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.TipoDomicilio import TipoDomicilio
from apps.registro.models.Localidad import Localidad
from apps.registro.models.UnidadExtension import UnidadExtension
from django.core.exceptions import ValidationError


class UnidadExtensionDomicilio(models.Model):
    unidad_extension = models.ForeignKey(UnidadExtension, related_name = 'unidad_extension_domicilio', editable = False)
    tipo_domicilio = models.ForeignKey(TipoDomicilio)
    localidad = models.ForeignKey(Localidad, related_name = 'unidad_extension_localidad')
    calle = models.CharField(max_length = 100)
    altura = models.CharField(max_length = 5)
    referencia = models.CharField(max_length = 255, null = True, blank = True)
    cp = models.CharField(max_length = 20)

    class Meta:
        app_label = 'registro'
        db_table = 'registro_unidad_extension_domicilio'

    def __unicode__(self):
        if self.cp:
            cp = " (CP: " + self.cp + ")"
        else:
            cp = ""
        return str(self.calle) + " " + str(self.altura) + " - " + self.localidad.nombre + cp

    def __init__(self, *args, **kwargs):
        super(UnidadExtensionDomicilio, self).__init__(*args, **kwargs)
