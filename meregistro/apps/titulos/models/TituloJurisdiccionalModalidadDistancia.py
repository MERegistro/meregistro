# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.TituloJurisdiccional import TituloJurisdiccional


class TituloJurisdiccionalModalidadDistancia(models.Model):
    titulo = models.ForeignKey(TituloJurisdiccional, related_name = 'modalidad_distancia')
    duracion = models.PositiveIntegerField()
    cuatrimestres = models.PositiveIntegerField(null = True, blank = True)
    nro_dictamen = models.CharField(max_length = 50, null = True, blank = True)

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_titulo_jurisd_modalidad_distancia'
        ordering = ['id']

    def __unicode__(self):
        return self.titulo



