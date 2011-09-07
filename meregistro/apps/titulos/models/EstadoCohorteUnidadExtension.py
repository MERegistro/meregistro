# -*- coding: utf-8 -*-
from django.db import models
"""
Representa las opciones de estados que tiene cada cohorte asignada a un anexo
"""

class EstadoCohorteUnidadExtension(models.Model):

    ASIGNADA = u'Asignada'
    ACEPTADA = u'Aceptada por unidad de extensión'
    REGISTRADA = u'Registrada'

    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'titulos'
        ordering = ['nombre']
        db_table = 'titulos_estado_cohorte_unidad_extension'

    def __unicode__(self):
        return self.nombre
