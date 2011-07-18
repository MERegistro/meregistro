# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models import EstadoTituloOrientacion, TituloOrientacion


class TituloOrientacionEstado(models.Model):
    titulo_orientacion = models.ForeignKey(TituloOrientacion)
    estado = models.ForeignKey(EstadoTituloOrientacion)
    fecha = models.DateField()

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_titulo_orientacion_estados'

    def __unicode__(self):
        return self.estado.nombre
