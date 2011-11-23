# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.CohorteExtensionAulica import CohorteExtensionAulica
from apps.titulos.models.EstadoCohorteExtensionAulica import EstadoCohorteExtensionAulica
import datetime

"""
Representa los estados por los que pasa cada cohorte de extensión áulica
"""

class CohorteExtensionAulicaEstado(models.Model):
    cohorte_extension_aulica = models.ForeignKey(CohorteExtensionAulica)
    estado = models.ForeignKey(EstadoCohorteExtensionAulica)
    fecha = models.DateField()

    class Meta:
        app_label = 'titulos'
        ordering = ['fecha']
        db_table = 'titulos_cohorte_extension_aulica_estados'

    def __unicode__(self):
        return str(self.cohorte_extension_aulica.cohorte.anio)
