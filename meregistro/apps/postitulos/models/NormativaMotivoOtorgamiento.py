# -*- coding: utf-8 -*-
from django.db import models
"""
Representa las opciones del motivo de otorgamiento de una normativa
"""

class NormativaMotivoOtorgamiento(models.Model):

    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'postitulos'
        ordering = ['nombre']
        db_table = 'postitulos_normativa_motivo_otorgamiento'

    def __unicode__(self):
        return self.nombre
