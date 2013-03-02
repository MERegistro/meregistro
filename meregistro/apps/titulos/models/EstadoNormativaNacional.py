# -*- coding: utf-8 -*-
from django.db import models
"""
Representa las opciones de estados que tiene cada normativa nacional
"""

class EstadoNormativaNacional(models.Model):

    NO_VIGENTE = u'No vigente'
    VIGENTE = u'Vigente'

    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'titulos'
        ordering = ['nombre']
        db_table = 'titulos_estado_normativa_nacional'

    def __unicode__(self):
        return self.nombre
