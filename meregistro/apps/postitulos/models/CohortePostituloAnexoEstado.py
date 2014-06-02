# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models.CohortePostituloAnexo import CohortePostituloAnexo
from apps.postitulos.models.EstadoCohortePostituloAnexo import EstadoCohortePostituloAnexo
import datetime

"""
Representa los estados por los que pasa cada cohorte de anexo
"""

class CohortePostituloAnexoEstado(models.Model):
    cohorte_postitulo_anexo = models.ForeignKey(CohortePostituloAnexo)
    estado = models.ForeignKey(EstadoCohortePostituloAnexo)
    fecha = models.DateField()

    class Meta:
        app_label = 'postitulos'
        ordering = ['fecha']
        db_table = 'postitulos_cohorte_postitulo_anexo_estados'

    def __unicode__(self):
        return str(self.cohorte_postitulo_anexo.cohorte.anio)
