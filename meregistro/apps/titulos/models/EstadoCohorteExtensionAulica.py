# -*- coding: utf-8 -*-
from django.db import models
"""
Representa las opciones de estados que tiene cada cohorte asignada a un anexo
"""

class EstadoCohorteExtensionAulica(models.Model):

    ASIGNADA = u'Asignada'
    ACEPTADA = u'Aceptada por extensión áulica'
    REGISTRADA = u'Registrada'

    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'titulos'
        ordering = ['nombre']
        db_table = 'titulos_estado_cohorte_extension_aulica'

    def __unicode__(self):
        return self.nombre
