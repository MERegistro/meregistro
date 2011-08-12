# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.CohorteEstablecimiento import CohorteEstablecimiento
from apps.titulos.models.EstadoCohorteEstablecimiento import EstadoCohorteEstablecimiento
import datetime

"""
Representa los estados por los que pasa cada título jurisdiccional
"""

class CohorteEstablecimientoEstado(models.Model):
    cohorte_establecimiento = models.ForeignKey(CohorteEstablecimiento)
    estado = models.ForeignKey(EstadoCohorteEstablecimiento)
    fecha = models.DateField()

    class Meta:
        app_label = 'titulos'
        ordering = ['fecha']
        db_table = 'titulos_cohorte_establecimiento_estados'

    def __unicode__(self):
        return str(self.cohorte_establecimiento.cohorte.anio)
