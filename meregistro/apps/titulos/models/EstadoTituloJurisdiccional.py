# -*- coding: utf-8 -*-
from django.db import models
"""
Representa las opciones de estados que tiene cada título jurisdiccional
"""

class EstadoTituloJurisdiccional(models.Model):

    SIN_CONTROLAR = u'Sin controlar'
    CONTROLADO = u'Controlado'
    REGISTRADO= u'Registrado'

    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'titulos'
        ordering = ['nombre']
        db_table = 'titulos_estado_titulo_jurisdiccional'

    def __unicode__(self):
        return self.nombre
