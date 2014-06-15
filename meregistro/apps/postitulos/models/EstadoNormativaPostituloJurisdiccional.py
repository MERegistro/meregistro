# -*- coding: utf-8 -*-
from django.db import models
"""
Representa las opciones de estados que tiene cada normativa jurisdiccional
"""

class EstadoNormativaPostituloJurisdiccional(models.Model):

    NO_VIGENTE = u'No vigente'
    VIGENTE = u'Vigente'

    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'postitulos'
        ordering = ['nombre']
        db_table = 'postitulos_estado_normativa_postitulo_jurisdiccional'

    def __unicode__(self):
        return self.nombre
