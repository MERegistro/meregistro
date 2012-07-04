# -*- coding: utf-8 -*-
from django.db import models


class Turno(models.Model):

    TURNO_MANIANA = 'Mañana'
    TURNO_TARDE = 'Tarde'
    TURNO_NOCHE = 'Noche'
    
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = 'registro'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre
