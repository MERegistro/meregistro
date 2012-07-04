# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.ExtensionAulica import ExtensionAulica
from django.core.exceptions import ValidationError
import datetime


class ExtensionAulicaBaja(models.Model):
    extension_aulica = models.ForeignKey(ExtensionAulica)
    observaciones = models.CharField(max_length = 255)
    fecha_baja = models.DateField()

    class Meta:
        app_label = 'registro'
        db_table = 'registro_extension_aulica_baja'

    def __unicode__(self):
        return self.fecha_baja
