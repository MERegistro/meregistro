# -*- coding: utf-8 -*-
from django.db import models
"""
Representa las opciones de estados que tiene cada título nacional
"""

class EstadoSolicitud(models.Model):

    PENDIENTE = u'Pendiente'
    CONTROLADO = u'Controlado'

    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = 'validez_nacional'
        ordering = ['nombre']
        db_table = 'validez_nacional_estado_solicitud'

    def __unicode__(self):
        return self.nombre
