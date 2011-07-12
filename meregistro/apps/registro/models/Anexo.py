# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.Estado import Estado
from apps.registro.models.Turno import Turno
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import datetime


class Anexo(models.Model):
    establecimiento = models.ForeignKey(Establecimiento)
    cue = models.CharField(max_length = 2, help_text = u'2 dígitos, ej: 01...02')
    fecha_alta = models.DateField(null = True, blank = True)
    nombre = models.CharField(max_length = 255)
    telefono = models.CharField(max_length = 100, null = True, blank = True)
    email = models.EmailField(max_length = 255, null = True, blank = True)
    sitio_web = models.URLField(max_length = 255, null = True, blank = True, verify_exists = False)
    turnos = models.ManyToManyField(Turno, null = True, db_table = 'registro_anexos_turnos')

    class Meta:
        app_label = 'registro'

    def __unicode__(self):
        return self.nombre

    " Sobreescribo el init para agregarle propiedades "
    def __init__(self, *args, **kwargs):
        super(Anexo, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()
        self.estado_actual = self.getEstadoActual()

    def clean(self):
        " Chequea que la combinación entre establecimiento y cue sea único "
        cue = self.cue
        establecimiento = self.establecimiento_id
        if cue and establecimiento:
            try:
                anexo = Anexo.objects.get(cue=self.cue, establecimiento__cue__exact=self.establecimiento.cue)
                if anexo and anexo != self:
                    raise ValidationError('Ya existe un anexo con ese CUE en ese establecimiento.')
            except Anexo.DoesNotExist:
                pass

    def registrar_estado(self, estado):
        from apps.registro.models.AnexoEstado import AnexoEstado
        registro = AnexoEstado(estado = estado)
        registro.fecha = datetime.date.today()
        registro.anexo_id = self.id
        registro.save()

    def getEstados(self):
        from apps.registro.models.AnexoEstado import AnexoEstado
        try:
            estados = AnexoEstado.objects.filter(anexo = self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados

    def getEstadoActual(self):
        try:
            return list(self.estados)[-1]
        except IndexError:
            return None

    def registrarBaja(self, baja):
        from apps.registro.models.AnexoBaja import AnexoBaja
        estado = Estado.objects.get(nombre = Estado.BAJA)
        self.registrar_estado(estado)
        baja.anexo = self
        baja.save()

    def dadoDeBaja(self):
        from apps.registro.models.AnexoBaja import AnexoBaja
        try:
            baja = AnexoBaja.objects.get(anexo = self)
        except ObjectDoesNotExist:
            return False
        return True

