# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.CohorteUnidadExtension import CohorteUnidadExtension
from apps.titulos.models.EstadoCohorteUnidadExtension import EstadoCohorteUnidadExtension
import datetime

"""
Representa los estados por los que pasa cada cohorte de unidad de extensión
"""

class CohorteUnidadExtensionEstado(models.Model):
    cohorte_unidad_extension = models.ForeignKey(CohorteUnidadExtension)
    estado = models.ForeignKey(EstadoCohorteUnidadExtension)
    fecha = models.DateField()

    class Meta:
        app_label = 'titulos'
        ordering = ['fecha']
        db_table = 'titulos_cohorte_unidad_extension_estados'

    def __unicode__(self):
        return str(self.cohorte_unidad_extension.cohorte.anio)
