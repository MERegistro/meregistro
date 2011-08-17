# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.CohorteEstablecimiento import CohorteEstablecimiento
import datetime

"Seguimiento de cada cohorte del establecimiento"
class CohorteSeguimiento(models.Model):
    cohorte_establecimiento = models.ForeignKey(CohorteEstablecimiento, editable = False, related_name = 'seguimiento')
    solo_cursan_nueva = models.PositiveIntegerField(null = True, blank = True)
    solo_recursan = models.PositiveIntegerField(null = True, blank = True)
    recursan_cursan = models.PositiveIntegerField(null = True, blank = True)
    no_cursan = models.PositiveIntegerField(null = True, blank = True)
    observaciones = models.CharField(max_length = 255, null = True, blank = True)

    class Meta:
        app_label = 'titulos'
        ordering = ['cohorte_establecimiento__cohorte__anio']
        db_table = 'titulos_cohorte_seguimiento'

    def __unicode__(self):
        return str(self.cohorte_establecimiento.cohorte.anio)

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(CohorteSeguimiento, self).__init__(*args, **kwargs)
