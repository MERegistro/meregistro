# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.CarreraJurisdiccional import CarreraJurisdiccional
from apps.titulos.models.EstadoCarreraJurisdiccional import EstadoCarreraJurisdiccional
import datetime

"""
Representa los estados por los que pasa cada carrera jurisdiccional
"""

class CarreraJurisdiccionalEstado(models.Model):
    carrera_jurisdiccional = models.ForeignKey(CarreraJurisdiccional)
    estado = models.ForeignKey(EstadoCarreraJurisdiccional)
    fecha = models.DateField()

    class Meta:
        app_label = 'titulos'
        ordering = ['fecha']
        db_table = 'titulos_carrera_jurisdiccional_estados'

    def __unicode__(self):
        return str(self.titulo.nombre) + " - " + str(self.estado.nombre) + " - " + self.fecha
