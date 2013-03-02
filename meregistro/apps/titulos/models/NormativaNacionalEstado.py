# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.NormativaNacional import NormativaNacional
from apps.titulos.models.EstadoNormativaNacional import EstadoNormativaNacional

"""
Representa los estados por los que pasa cada normativa nacional
"""

class NormativaNacionalEstado(models.Model):
    normativa_nacional = models.ForeignKey(NormativaNacional)
    estado = models.ForeignKey(EstadoNormativaNacional)
    fecha = models.DateField()

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_normativa_nacional_estados'

    def __unicode__(self):
        return self.estado.nombre
