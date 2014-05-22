# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models.CarreraPostitulo import CarreraPostitulo
from apps.postitulos.models.EstadoCarreraPostitulo import EstadoCarreraPostitulo
import datetime

"""
Representa los estados por los que pasa cada carrera
"""

class CarreraPostituloEstado(models.Model):
    carrera_postitulo = models.ForeignKey(CarreraPostitulo)
    estado = models.ForeignKey(EstadoCarreraPostitulo)
    fecha = models.DateField()

    NO_VIGENTE = u'No vigente'
    VIGENTE = u'Vigente'

    class Meta:
        app_label = 'postitulos'
        ordering = ['fecha']
        db_table = 'postitulos_carrera_postitulo_estados'

    def __unicode__(self):
        return str(self.carrera_postitulo.nombre) + " - " + str(self.estado.nombre) + " - " + self.fecha
