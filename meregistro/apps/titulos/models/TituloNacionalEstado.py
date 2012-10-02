# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.TituloNacional import TituloNacional
from apps.titulos.models.EstadoTituloNacional import EstadoTituloNacional
import datetime

"""
Representa los estados por los que pasa cada título
"""

class TituloNacionalEstado(models.Model):
    titulo_nacional = models.ForeignKey(TituloNacional)
    estado = models.ForeignKey(EstadoTituloNacional)
    fecha = models.DateField()

    class Meta:
        app_label = 'titulos'
        ordering = ['fecha']
        db_table = 'titulos_titulo_nacional_estados'

    def __unicode__(self):
        return str(self.titulo_nacional.nombre) + " - " + str(self.estado.nombre) + " - " + self.fecha
