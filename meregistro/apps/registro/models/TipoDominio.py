# -*- coding: utf-8 -*-
from django.db import models


class TipoDominio(models.Model):

    TIPO_EXCLUSIVO = 'Exclusivo'
    TIPO_COMPARTIDO = 'Compartido'
    
    descripcion = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = 'registro'
        db_table = 'registro_tipo_dominio'
        ordering = ['descripcion']

    def __unicode__(self):
        return self.descripcion
