# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.TituloJurisdiccional import TituloJurisdiccional


class TituloJurisdiccionalModalidadPresencial(models.Model):
    titulo = models.ForeignKey(TituloJurisdiccional, related_name = 'modalidad_presencial')
    duracion = models.PositiveIntegerField(null = True, blank = True)
    cuatrimestres = models.PositiveIntegerField(null = True, blank = True)

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_titulo_jurisd_modalidad_presencial'
        ordering = ['id']

    def __unicode__(self):
        return self.titulo
