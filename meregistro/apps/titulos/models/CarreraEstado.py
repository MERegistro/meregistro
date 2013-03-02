# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.Carrera import Carrera
from apps.titulos.models.EstadoCarrera import EstadoCarrera
import datetime

"""
Representa los estados por los que pasa cada carrera
"""

class CarreraEstado(models.Model):
    carrera = models.ForeignKey(Carrera)
    estado = models.ForeignKey(EstadoCarrera)
    fecha = models.DateField()

    NO_VIGENTE = u'No vigente'
    VIGENTE = u'Vigente'

    class Meta:
        app_label = 'titulos'
        ordering = ['fecha']
        db_table = 'titulos_carrera_estados'

    def __unicode__(self):
        return str(self.carrera.nombre) + " - " + str(self.estado.nombre) + " - " + self.fecha
