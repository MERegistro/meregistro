# -*- coding: utf-8 -*-
from django.db import models
"""
Representa las opciones de estados que tiene cada cohorte asignada a un anexo
"""

class EstadoCohorteAnexo(models.Model):

    ASIGNADA = u'Aceptada'
    REGISTRADA = u'Registrada'
    RECHAZADA = u'Rechazada'
    FINALIZADA = u'Finalizada'

    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'titulos'
        ordering = ['nombre']
        db_table = 'titulos_estado_cohorte_anexo'

    def __unicode__(self):
        return self.nombre
