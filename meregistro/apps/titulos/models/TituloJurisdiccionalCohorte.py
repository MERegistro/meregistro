# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.TituloJurisdiccional import TituloJurisdiccional


class TituloJurisdiccionalCohorte(models.Model):
    titulo = models.ForeignKey(TituloJurisdiccional)
    cohortes_aprobadas = models.PositiveIntegerField()
    anio_primera_cohorte = models.PositiveIntegerField()
    anio_ultima_cohorte = models.PositiveIntegerField()
    observaciones = models.CharField(max_length = 255, null = True, blank = True)

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_titulo_jurisd_cohorte'
        ordering = ['id']

    def __unicode__(self):
        return self.titulo
