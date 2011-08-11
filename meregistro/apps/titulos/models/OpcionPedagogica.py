# -*- coding: utf-8 -*-
from django.db import models

class OpcionPedagogica(models.Model):
    nombre = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.nombre

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_opcion_pedagogica'
