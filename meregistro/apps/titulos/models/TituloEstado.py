# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.Titulo import Titulo
from apps.titulos.models.EstadoTitulo import EstadoTitulo
import datetime

class TituloEstado(models.Model):
    titulo = models.ForeignKey(Titulo)
    estado = models.ForeignKey(EstadoTitulo)
    fecha = models.DateField()

    class Meta:
        app_label = 'titulos'
        ordering = ['fecha']
        db_table = 'titulos_titulo_estado'

    def __unicode__(self):
        return str(self.titulo.nombre) + " - " + str(self.estado.nombre) + " - " + self.fecha
