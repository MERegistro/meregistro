# -*- coding: utf-8 -*-
from django.db import models


class TipoNormativaPostituloJurisdiccional(models.Model):
    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'postitulos'
        ordering = ['nombre']
        db_table = 'postitulos_tipo_normativa_postitulo_jurisdiccional'

    def __unicode__(self):
        return self.nombre
