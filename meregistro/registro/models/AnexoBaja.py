# -*- coding: utf-8 -*-
from django.db import models
from registro.models.Anexo import Anexo
from django.core.exceptions import ValidationError
import datetime


class AnexoBaja(models.Model):
    anexo = models.ForeignKey(Anexo)
    observaciones = models.CharField(max_length = 255)
    fecha_baja = models.DateField()

    class Meta:
        app_label = 'registro'
        db_table = 'registro_anexo_baja'

    def __unicode__(self):
        return self.fecha_baja
