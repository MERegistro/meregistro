# -*- coding: utf-8 -*-
from django.db import models
from registro.models.UnidadExtension import UnidadExtension
from django.core.exceptions import ValidationError
import datetime


class UnidadExtensionBaja(models.Model):
    unidad_extension = models.ForeignKey(UnidadExtension)
    observaciones = models.CharField(max_length = 255)
    fecha_baja = models.DateField()

    class Meta:
        app_label = 'registro'
        db_table = 'registro_unidad_extension_baja'

    def __unicode__(self):
        return self.fecha_baja
