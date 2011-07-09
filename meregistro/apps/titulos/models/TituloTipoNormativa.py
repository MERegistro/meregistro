# -*- coding: utf-8 -*-
from django.db import models


class TituloTipoNormativa(models.Model):
    descripcion = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_tipo_normativa'
        ordering = ['descripcion']

    def __unicode__(self):
        return self.descripcion
