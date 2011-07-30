# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.TituloJurisdiccional import TituloJurisdiccional
from apps.titulos.models.EstadoTituloJurisdiccional import EstadoTituloJurisdiccional
import datetime

"""
Representa los estados por los que pasa cada título jurisdiccional
"""

class TituloJurisdiccionalEstado(models.Model):
    titulo = models.ForeignKey(TituloJurisdiccional)
    estado = models.ForeignKey(EstadoTituloJurisdiccional)
    fecha = models.DateField()

    class Meta:
        app_label = 'titulos'
        ordering = ['fecha']
        db_table = 'titulos_titulo_jurisd_estados'

    def __unicode__(self):
        return str(self.titulo.nombre) + " - " + str(self.estado.nombre) + " - " + self.fecha
