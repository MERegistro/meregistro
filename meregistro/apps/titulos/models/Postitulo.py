# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.TipoProyecto import TipoProyecto
from apps.registro.models.Establecimiento import Establecimiento
from apps.titulos.models import OpcionPedagogica, TipoHora, TipoNormativaJurisdiccional, EstadoTramitePostitulo
import datetime

YEARS_CHOICES = tuple((int(n), str(n)) for n in range(2010, datetime.datetime.now().year + 1))

class Postitulo(models.Model):
    anio = models.IntegerField(choices = YEARS_CHOICES)
    nombre = models.CharField(max_length = 50)
    opcion_pedagogica = models.ForeignKey(OpcionPedagogica)
    duracion_anios = models.PositiveIntegerField()
    duracion_cuatrimestres = models.IntegerField(choices = [(0,0), (1,1)], null=True, blank=True)
    primera_cohorte_autorizada = models.IntegerField(choices = YEARS_CHOICES)
    ultima_cohorte_autorizada = models.IntegerField(choices = YEARS_CHOICES)
    ingresantes_09_10 = models.PositiveIntegerField()
    egresados_09_10 = models.PositiveIntegerField()
    tipo_horas = models.ForeignKey(TipoHora)
    cantidad_horas = models.PositiveIntegerField()
    tipo_normativa = models.ForeignKey(TipoNormativaJurisdiccional)
    normativa = models.CharField(max_length = 100)
    estado_tramite = models.ForeignKey(EstadoTramitePostitulo)
    resolucion_validez_nacional = models.CharField(max_length = 100, null=True, blank=True)
    nro_dictamen_cfr_epoe = models.CharField(max_length = 100, null=True, blank=True)
    fecha_inicio = models.IntegerField(choices = YEARS_CHOICES, null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    establecimiento = models.ForeignKey(Establecimiento)
    observaciones = models.CharField(max_length = 255, null = True, blank = True)

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_postitulo'
