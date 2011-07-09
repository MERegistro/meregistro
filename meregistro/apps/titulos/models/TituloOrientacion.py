# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.Titulo import Titulo


class TituloOrientacion(models.Model):
    nombre = models.CharField(max_length = 50, unique = True)
    titulo = models.ForeignKey(Titulo)

    class Meta:
        app_label = 'titulos'
        ordering = ['nombre']
        db_table = 'titulos_titulo_orientaciones'

    def __unicode__(self):
        return self.nombre
