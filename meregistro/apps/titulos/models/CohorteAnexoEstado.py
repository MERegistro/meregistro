# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.CohorteAnexo import CohorteAnexo
from apps.titulos.models.EstadoCohorteAnexo import EstadoCohorteAnexo
import datetime

"""
Representa los estados por los que pasa cada cohorte de anexo
"""

class CohorteAnexoEstado(models.Model):
    cohorte_anexo = models.ForeignKey(CohorteAnexo)
    estado = models.ForeignKey(EstadoCohorteAnexo)
    fecha = models.DateField()

    class Meta:
        app_label = 'titulos'
        ordering = ['fecha']
        db_table = 'titulos_cohorte_anexo_estados'

    def __unicode__(self):
        return str(self.cohorte_anexo.cohorte.anio)
