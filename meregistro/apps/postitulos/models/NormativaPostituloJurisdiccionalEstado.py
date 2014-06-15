# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models.NormativaPostituloJurisdiccional import NormativaPostituloJurisdiccional
from apps.postitulos.models.EstadoNormativaPostituloJurisdiccional import EstadoNormativaPostituloJurisdiccional

"""
Representa los estados por los que pasa cada normativa jurisdiccional
"""

class NormativaPostituloJurisdiccionalEstado(models.Model):
    normativa_postitulo_jurisdiccional = models.ForeignKey(NormativaPostituloJurisdiccional)
    estado = models.ForeignKey(EstadoNormativaPostituloJurisdiccional)
    fecha = models.DateField()

    class Meta:
        app_label = 'postitulos'
        db_table = 'postitulos_normativa_postitulo_jurisdiccional_estados'

    def __unicode__(self):
        return self.estado.nombre
