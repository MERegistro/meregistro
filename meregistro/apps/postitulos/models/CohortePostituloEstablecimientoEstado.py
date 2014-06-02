# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models.CohortePostituloEstablecimiento import CohortePostituloEstablecimiento
from apps.postitulos.models.EstadoCohortePostituloEstablecimiento import EstadoCohortePostituloEstablecimiento
import datetime

"""
Representa los estados por los que pasa cada cohorte del establecimiento
"""

class CohortePostituloEstablecimientoEstado(models.Model):
    cohorte_postitulo_establecimiento = models.ForeignKey(CohortePostituloEstablecimiento)
    estado = models.ForeignKey(EstadoCohortePostituloEstablecimiento)
    fecha = models.DateField()

    class Meta:
        app_label = 'postitulos'
        ordering = ['fecha']
        db_table = 'postitulos_cohorte_postitulo_establecimiento_estados'

    def __unicode__(self):
        return str(self.cohorte_postitulo_establecimiento.cohorte.anio)
