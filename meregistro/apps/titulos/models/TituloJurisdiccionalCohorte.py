# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.TituloJurisdiccional import TituloJurisdiccional

"Datos generales de cohorte para un título jurisdiccionals"
class TituloJurisdiccionalCohorte(models.Model):
    titulo_jurisdiccional = models.ForeignKey(TituloJurisdiccional, related_name = 'datos_cohorte')
    cohortes_aprobadas = models.PositiveIntegerField()
    anio_primera_cohorte = models.PositiveIntegerField()
    anio_ultima_cohorte = models.PositiveIntegerField()
    observaciones = models.CharField(max_length = 255, null = True, blank = True)

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_titulo_jurisd_cohorte'
        ordering = ['id']

    def __unicode__(self):
        return self.titulo_jurisdiccional
