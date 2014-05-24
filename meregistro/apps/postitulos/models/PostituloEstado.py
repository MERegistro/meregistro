# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models.Postitulo import Postitulo
from apps.postitulos.models.EstadoPostitulo import EstadoPostitulo
import datetime

"""
Representa los estados por los que pasa cada título
"""

class PostituloEstado(models.Model):
    postitulo = models.ForeignKey(Postitulo)
    estado = models.ForeignKey(EstadoPostitulo)
    fecha = models.DateField()

    class Meta:
        app_label = 'postitulos'
        ordering = ['fecha']
        db_table = 'postitulos_postitulo_estados'

    def __unicode__(self):
        return str(self.postitulo.nombre) + " - " + str(self.estado.nombre) + " - " + self.fecha
