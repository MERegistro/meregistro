# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.TipoNormativa import TipoNormativa
from apps.registro.models.Estado import Estado
from apps.registro.models.Turno import Turno
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import datetime

YEARS_CHOICES = tuple((int(n), str(n)) for n in range(1800, datetime.datetime.now().year + 1))

class UnidadExtension(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, editable = False)
    nombre = models.CharField(max_length = 255)
    observaciones = models.CharField(max_length = 255)
    tipo_normativa = models.ForeignKey(TipoNormativa)
    fecha_alta = models.DateField(null=True, blank=True)
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
        super(UnidadExtension, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()
        self.estado_actual = self.getEstadoActual()

    def __unicode__(self):
        return self.nombre

    def registrar_estado(self, estado):
        from apps.registro.models.UnidadExtensionEstado import UnidadExtensionEstado
        registro = UnidadExtensionEstado()
        registro.estado = estado
        registro.fecha = datetime.date.today()
        registro.unidad_extension_id = self.id
        registro.save()

    def getEstados(self):
        from apps.registro.models.UnidadExtensionEstado import UnidadExtensionEstado
        try:
            estados = UnidadExtensionEstado.objects.filter(unidad_extension = self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados

    def getEstadoActual(self):
        try:
            return list(self.estados)[-1].estado
        except IndexError:
            return None

    def registrarBaja(self, baja):
        from apps.registro.models.UnidadExtensionBaja import UnidadExtensionBaja
        estado = Estado.objects.get(nombre = Estado.BAJA)
        self.registrar_estado(estado)
        baja.unidad_extension = self
        baja.save()

    def dadaDeBaja(self):
        from apps.registro.models.UnidadExtensionBaja import UnidadExtensionBaja
        try:
            baja = UnidadExtensionBaja.objects.get(unidad_extension = self)
        except ObjectDoesNotExist:
            return False
        return True
