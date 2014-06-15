# -*- coding: utf-8 -*-
from django.db import models


class TipoPostitulo(models.Model):
    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'postitulos'
        ordering = ['nombre']
        db_table = 'postitulos_tipo_postitulo'

    def __unicode__(self):
        return self.nombre
