# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.Titulo import Titulo
from apps.titulos.models.EstadoTitulo import EstadoTitulo
import datetime

"""
Representa los estados por los que pasa cada título
"""

class TituloEstado(models.Model):
    titulo = models.ForeignKey(Titulo)
    estado = models.ForeignKey(EstadoTitulo)
    fecha = models.DateField()

    class Meta:
        app_label = 'titulos'
        ordering = ['fecha']
        db_table = 'titulos_titulo_estados'

    def __unicode__(self):
        return str(self.titulo.nombre) + " - " + str(self.estado.nombre) + " - " + self.fecha
