# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.TipoProyecto import TipoProyecto
from apps.registro.models.Establecimiento import Establecimiento
import datetime

class Proyecto(models.Model):
    tipo_proyecto = models.ForeignKey(TipoProyecto)
    nombre = models.CharField(max_length = 50)
    denominacion = models.CharField(max_length = 50)
    anio_presenta = models.PositiveIntegerField()
    cantidad_docentes_participantes = models.PositiveIntegerField()
    cantidad_escuelas_participantes = models.PositiveIntegerField()
    establecimiento = models.ForeignKey(Establecimiento)
    observaciones = models.CharField(max_length = 255, null = True, blank = True)

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_proyecto'

