# -*- coding: utf-8 -*-
from django.db import models


class PostituloTipoNormativa(models.Model):
    descripcion = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'postitulos'
        db_table = 'postitulos_tipo_normativa'
        ordering = ['descripcion']

    def __unicode__(self):
        return self.descripcion
