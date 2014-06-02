# -*- coding: utf-8 -*-
from django.db import models
"""
Representa las opciones de estados que tiene cada cohorte asignada a un anexo
"""

class EstadoCohortePostituloAnexo(models.Model):

    ASIGNADA = u'Aceptada'
    REGISTRADA = u'Registrada'
    RECHAZADA = u'Rechazada'

    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'postitulos'
        ordering = ['nombre']
        db_table = 'postitulos_estado_cohorte_postitulo_anexo'

    def __unicode__(self):
        return self.nombre
