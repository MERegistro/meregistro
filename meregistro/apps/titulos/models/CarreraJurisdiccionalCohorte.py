# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.CarreraJurisdiccional import CarreraJurisdiccional

"Datos generales de cohorte para una carrera jurisdiccional"
class CarreraJurisdiccionalCohorte(models.Model):
    carrera_jurisdiccional = models.ForeignKey(CarreraJurisdiccional, related_name='datos_cohorte')
    primera_cohorte_solicitada = models.PositiveIntegerField()
    ultima_cohorte_solicitada = models.PositiveIntegerField()
    primera_cohorte_autorizada = models.PositiveIntegerField(null=True)
    ultima_cohorte_autorizada = models.PositiveIntegerField(null=True)
    observaciones = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_carrera_jurisdiccional_cohorte'
        ordering = ['id']

    def __unicode__(self):
        return self.carrera_jurisdiccional
