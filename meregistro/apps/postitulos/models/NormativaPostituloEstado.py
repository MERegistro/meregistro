# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models.NormativaPostitulo import NormativaPostitulo
from apps.postitulos.models.EstadoNormativaPostitulo import EstadoNormativaPostitulo

"""
Representa los estados por los que pasa cada normativa
"""

class NormativaPostituloEstado(models.Model):
    normativa_postitulo = models.ForeignKey(NormativaPostitulo)
    estado = models.ForeignKey(EstadoNormativaPostitulo)
    fecha = models.DateField()

    class Meta:
        app_label = 'postitulos'
        db_table = 'postitulos_normativa_postitulos_estados'

    def __unicode__(self):
        return self.estado.nombre
