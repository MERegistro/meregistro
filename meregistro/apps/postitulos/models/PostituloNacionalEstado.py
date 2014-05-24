# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models.PostituloNacional import PostituloNacional
from apps.postitulos.models.EstadoPostituloNacional import EstadoPostituloNacional
import datetime

"""
Representa los estados por los que pasa cada título
"""

class PostituloNacionalEstado(models.Model):
    postitulo_nacional = models.ForeignKey(PostituloNacional)
    estado = models.ForeignKey(EstadoPostituloNacional)
    fecha = models.DateField()

    class Meta:
        app_label = 'postitulos'
        ordering = ['fecha']
        db_table = 'postitulos_postitulo_nacional_estados'

    def __unicode__(self):
        return str(self.postitulo_nacional.nombre) + " - " + str(self.estado.nombre) + " - " + self.fecha
