# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Anexo import Anexo
from apps.registro.models.Establecimiento import Establecimiento
import datetime

YEARS_CHOICES = tuple((int(n), str(n)) for n in range(1980, datetime.datetime.now().year + 1))

class Matricula(models.Model):
    anio_lectivo = models.IntegerField(choices = YEARS_CHOICES)
    matricula_solo_formacion_docente = models.PositiveIntegerField()
    matricula_positulos = models.PositiveIntegerField()
    matricula_solo_profesorados = models.PositiveIntegerField()    
    anexo = models.ForeignKey(Anexo, null = True, blank = True)
    establecimiento = models.ForeignKey(Establecimiento)
    observaciones = models.CharField(max_length = 255, null = True, blank = True)
    revisado_jurisdiccion = models.NullBooleanField(default=False, null=True)

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_matricula'

    def isDeletable(self):
        q = Matricula.objects.filter(anio_lectivo__gt=self.anio_lectivo)
        if self.establecimiento is not None:
            q.filter(establecimiento=self.establecimiento)
        if self.anexo is not None:
            q.filter(anexo=self.anexo)
        return len(q) == 0

    def isEditable(self):
        q = Matricula.objects.filter(anio_lectivo__gt=self.anio_lectivo)
        if self.establecimiento is not None:
            q.filter(establecimiento=self.establecimiento)
        if self.anexo is not None:
            q.filter(anexo=self.anexo)
        return len(q) == 0
        
