# -*- coding: utf-8 -*-
from django.db import models
"""
Representa las opciones de estados que tiene cada carrera
"""

class EstadoCarreraPostitulo(models.Model):

    NO_VIGENTE = u'No vigente'
    VIGENTE = u'Vigente'

    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'postitulos'
        ordering = ['nombre']
        db_table = 'postitulos_estado_carrera_postitulo'

    def __unicode__(self):
        return self.nombre
