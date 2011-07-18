# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.NormativaJurisdiccional import NormativaJurisdiccional
from apps.titulos.models.EstadoNormativaJurisdiccional import EstadoNormativaJurisdiccional

"""
Representa los estados por los que pasa cada normativa jurisdiccional
"""

class NormativaJurisdiccionalEstado(models.Model):
    normativa_jurisdiccional = models.ForeignKey(NormativaJurisdiccional)
    estado = models.ForeignKey(EstadoNormativaJurisdiccional)
    fecha = models.DateField()

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_normativa_jurisdiccional_estados'

    def __unicode__(self):
        return self.estado.nombre
