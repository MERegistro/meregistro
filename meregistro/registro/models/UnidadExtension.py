# -*- coding: utf-8 -*-
from django.db import models
from meregistro.registro.models.Establecimiento import Establecimiento
from meregistro.registro.models.TipoNormativa import TipoNormativa
from meregistro.registro.models.Estado import Estado
from meregistro.registro.models.Turno import Turno
from django.core.exceptions import ValidationError
import datetime

YEARS_CHOICES = tuple((int(n), str(n)) for n in range(1800, datetime.datetime.now().year + 1))

class UnidadExtension(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, editable = False)
    nombre = models.CharField(max_length = 255)
    observaciones = models.CharField(max_length = 255)
    tipo_normativa = models.ForeignKey(TipoNormativa)
    normativa = models.CharField(max_length = 100)
    anio_creacion = models.IntegerField(null=True, blank=True, choices = YEARS_CHOICES)
    sitio_web = models.URLField(max_length = 255, null = True, blank = True, verify_exists = False)
    telefono = models.CharField(max_length = 100, null = True, blank = True)
    email = models.EmailField(max_length = 255, null = True, blank = True)
    turnos = models.ManyToManyField(Turno, null = True, db_table = 'registro_unidades_extension_turnos')

    class Meta:
        app_label = 'registro'
        ordering = ['nombre']

    def __init__(self, *args, **kwargs):
        from meregistro.registro.models.UnidadExtensionEstado import UnidadExtensionEstado
        super(UnidadExtension, self).__init__(*args, **kwargs)
        self.registro_estados = UnidadExtensionEstado.objects.filter(unidad_extension = self).order_by('id')
        self.estado_actual = self.getEstadoActual()

    def __unicode__(self):
        return self.nombre

    def registrar_estado(self, estado):
        from meregistro.registro.models.UnidadExtensionEstado import UnidadExtensionEstado
        registro = UnidadExtensionEstado()
        registro.estado = estado
        registro.fecha = datetime.date.today()
        registro.unidad_extension_id = self.id
        registro.save()

    def estadoActual(self):
        try:
            return list(self.registro_estados)[-1].estado
        except IndexError:
            return None

    def getEstadoActual(self):
        estado_actual = self.estadoActual()
        if estado_actual is None:
            return u''
        return str(estado_actual)
