# -*- coding: utf-8 -*-
from django.db import models

class Area(models.Model):
    nombre = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'titulos'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre
