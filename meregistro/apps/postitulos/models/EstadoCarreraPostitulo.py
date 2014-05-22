# -*- coding: utf-8 -*-
from django.db import models
"""
Representa las opciones de estados que tiene cada carrera
"""

class EstadoCarrera(models.Model):

    NO_VIGENTE = u'No vigente'
    VIGENTE = u'Vigente'

    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'titulos'
        ordering = ['nombre']
        db_table = 'titulos_estado_carrera'

    def __unicode__(self):
        return self.nombre
