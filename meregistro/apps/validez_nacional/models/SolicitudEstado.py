# -*- coding: utf-8 -*-
from django.db import models
from apps.validez_nacional.models import Solicitud, EstadoSolicitud
import datetime

"""
Representa los estados por los que pasa cada título
"""

class SolicitudEstado(models.Model):
    solicitud = models.ForeignKey(Solicitud, null=False)
    estado = models.ForeignKey(EstadoSolicitud, null=False)
    fecha = models.DateField()

    class Meta:
        app_label = 'validez_nacional'
        ordering = ['fecha']
        db_table = 'validez_nacional_solicitud_estados'

    def __unicode__(self):
        return str(self.estado.nombre) + " - " + self.fecha
