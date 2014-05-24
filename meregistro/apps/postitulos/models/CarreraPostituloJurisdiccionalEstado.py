# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models.CarreraPostituloJurisdiccional import CarreraPostituloJurisdiccional
from apps.postitulos.models.EstadoCarreraPostituloJurisdiccional import EstadoCarreraPostituloJurisdiccional
import datetime

"""
Representa los estados por los que pasa cada carrera jurisdiccional
"""

class CarreraJurisdiccionalEstado(models.Model):
    carrera_postitulo_jurisdiccional = models.ForeignKey(CarreraPostituloJurisdiccional)
    estado = models.ForeignKey(EstadoCarreraPostituloJurisdiccional)
    fecha = models.DateField()

    class Meta:
        app_label = 'postitulos'
        ordering = ['fecha']
        db_table = 'postitulos_carrera_postitulo_jurisdiccional_estados'

    def __unicode__(self):
        return str(self.postitulo.nombre) + " - " + str(self.estado.nombre) + " - " + self.fecha
