# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.CarreraJurisdiccional import CarreraJurisdiccional

"Datos generales de cohorte para una carrera jurisdiccional"
class CarreraJurisdiccionalCohorte(models.Model):
    carrera_jurisdiccional = models.ForeignKey(CarreraJurisdiccional, related_name='datos_cohorte')
    anio_primera_cohorte = models.PositiveIntegerField(null=True)
    anio_ultima_cohorte = models.PositiveIntegerField(null=True)
    cohortes_aprobadas = models.PositiveIntegerField(null=True)    
    observaciones = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_carrera_jurisdiccional_cohorte'
        ordering = ['id']

    def __unicode__(self):
        return self.carrera_jurisdiccional
