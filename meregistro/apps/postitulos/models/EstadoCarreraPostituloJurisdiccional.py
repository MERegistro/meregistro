# -*- coding: utf-8 -*-
from django.db import models
"""
Representa las opciones de estados que tiene cada carrera jurisdiccional
"""

class EstadoCarreraPostituloJurisdiccional(models.Model):

    SIN_CONTROLAR = u'Sin controlar'
    CONTROLADO = u'Controlado'
    REGISTRADO = u'Registrado'

    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'postitulos'
        ordering = ['nombre']
        db_table = '[postitulos_estado_carrera_postitulo_jurisdiccional'

    def __unicode__(self):
        return self.nombre
