# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models.CohortePostituloExtensionAulica import CohortePostituloExtensionAulica
from apps.titulos.models.EstadoCohortePostituloExtensionAulica import EstadoCohortePostituloExtensionAulica
import datetime

"""
Representa los estados por los que pasa cada cohorte de extensión áulica
"""

class CohortePostituloExtensionAulicaEstado(models.Model):
    cohorte_postitulo_extension_aulica = models.ForeignKey(CohortePostituloExtensionAulica)
    estado = models.ForeignKey(EstadoCohortePostituloExtensionAulica)
    fecha = models.DateField()

    class Meta:
        app_label = 'postitulos'
        ordering = ['fecha']
        db_table = 'postitulos_cohorte_psotitulo_extension_aulica_estados'

    def __unicode__(self):
        return str(self.cohorte_postitulo_extension_aulica.cohorte.anio)
