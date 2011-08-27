# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Anexo import Anexo
import datetime

YEARS_CHOICES = tuple((int(n), str(n)) for n in range(2010, datetime.datetime.now().year + 1))

class Matricula(models.Model):
    anio_lectivo = models.IntegerField(choices = YEARS_CHOICES)
    matricula_solo_formacion_docente = models.PositiveIntegerField()
    matricula_positulos = models.PositiveIntegerField()
    matricula_solo_profesorados = models.PositiveIntegerField()    
    anexo = models.ForeignKey(Anexo)
    observaciones = models.CharField(max_length = 255, null = True, blank = True)

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_matricula'

    def isDeletable(self):
        return self.anio_lectivo == datetime.date.today().year

    def isEditable(self):
        return self.anio_lectivo == datetime.date.today().year
        
