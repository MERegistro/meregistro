# -*- coding: utf-8 -*-
from django.db import models
"""
Representa las opciones de estados que tiene cada cohorte asignada a un establecimiento
"""

class EstadoCohortePostituloEstablecimiento(models.Model):

    ASIGNADA = u'Aceptada'
    REGISTRADA = u'Registrada'
    RECHAZADA = u'Rechazada'

    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'postitulos'
        ordering = ['nombre']
        db_table = 'postitulos_estado_cohorte_postitulo_establecimiento'

    def __unicode__(self):
        return self.nombre
