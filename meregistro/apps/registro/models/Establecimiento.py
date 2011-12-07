# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.TipoNormativa import TipoNormativa
from apps.registro.models.Jurisdiccion import Jurisdiccion
from apps.registro.models.RegistroEstablecimiento import RegistroEstablecimiento
from apps.registro.models.DependenciaFuncional import DependenciaFuncional
from apps.registro.models.Nivel import Nivel
from apps.registro.models.Funcion import Funcion
from apps.registro.models.Turno import Turno
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from apps.seguridad.models import Ambito
import datetime

YEARS_CHOICES = tuple((int(n), str(n)) for n in range(1800, datetime.datetime.now().year + 1))


class Establecimiento(models.Model):
    dependencia_funcional = models.ForeignKey(DependenciaFuncional)
    cue = models.CharField(max_length = 5)
    nombre = models.CharField(max_length = 255)
    tipo_normativa = models.ForeignKey(TipoNormativa)
    unidad_academica = models.BooleanField()
    nombre_unidad_academica = models.CharField(max_length = 100, null = True, blank = True)
    identificacion_provincial = models.CharField(max_length = 100, null = True, blank = True)
    posee_subsidio = models.BooleanField()
    norma_creacion = models.CharField(max_length = 100)
    observaciones = models.TextField(max_length = 255, null = True, blank = True)
    anio_creacion = models.IntegerField(null = True, blank = True, choices = YEARS_CHOICES)
    telefono = models.CharField(max_length = 100, null = True, blank = True)
    fax = models.CharField(max_length = 100, null = True, blank = True)
    email = models.EmailField(max_length = 255, null = True, blank = True)
    sitio_web = models.URLField(max_length = 255, null = True, blank = True, verify_exists = False)
    ambito = models.ForeignKey(Ambito, editable = False, null = True)
    turnos = models.ManyToManyField(Turno, blank = True, null = True, db_table = 'registro_establecimientos_turnos')
    niveles = models.ManyToManyField(Nivel, blank = True, null = True, db_table = 'registro_establecimientos_niveles')
    funciones = models.ManyToManyField(Funcion, blank = True, null = True, db_table = 'registro_establecimientos_funciones')
    estado = models.ForeignKey(EstadoEstablecimiento, editable = False, null = True)
    old_id = models.IntegerField(null = True, blank = True, editable = False)

    class Meta:
        app_label = 'registro'
        ordering = ['nombre']

    """
    Sobreescribo el init para agregarle propiedades
    """
    def __init__(self, *args, **kwargs):
        super(Establecimiento, self).__init__(*args, **kwargs)
        self.registro_estados = RegistroEstablecimiento.objects.filter(establecimiento = self).order_by('id')
        self.estado_actual = self.getEstadoActual()

    def __unicode__(self):
        return str(self.cue) + ' - ' + self.nombre

    def clean(self):
        #Chequea que la combinación entre jurisdiccion y cue sea única
        try:
            est = Establecimiento.objects.get(cue = self.cue, dependencia_funcional__jurisdiccion__id = self.dependencia_funcional.jurisdiccion.id)
            if est and est != self:
                raise ValidationError('Ya existe un establecimiento con ese CUE en su jurisdicción.')
        except ObjectDoesNotExist:
            pass

    def registrar_estado(self, estado, observaciones = ''):
        registro = RegistroEstablecimiento(estado = estado)
        registro.fecha = datetime.date.today()
        registro.establecimiento_id = self.id
        registro.observaciones = observaciones
        self.estado = estado
        registro.save()
        self.save()

    def save(self):
        self.updateAmbito()
        if self.id is not None:
            self.ambito.vigente = (self.estado.nombre != EstadoEstablecimiento.PENDIENTE)
        self.ambito.save()
        models.Model.save(self)

    def delete(self):
        estado = EstadoEstablecimiento.objects.get(nombre = EstadoEstablecimiento.BAJA)
        self.registrar_estado(estado)

    def updateAmbito(self):
        if self.pk is None or self.ambito is None:
            try:
                self.ambito = self.dependencia_funcional.ambito.createChild(self.nombre)
            except Exception:
                pass
        else:
            self.ambito.descripcion = self.nombre
            self.ambito.save()

    def hasAnexos(self):
        from apps.registro.models.Anexo import Anexo
        anexos = Anexo.objects.filter(establecimiento = self)
        return anexos.count() > 0

    def getEstadoActual(self):
        estado_actual = self.estadoActual()
        if estado_actual is None:
            return u''
        return str(estado_actual)

    def estadoActual(self):
        try:
            return list(self.registro_estados)[-1].estado
        except IndexError:
            return None

    """
    Se puede eliminar cuando:
     * Tiene un sólo estado y es pendiente
     (hoy día si tiene un sólo estado ES pendiente)
    """
    def isDeletable(self):
        cant_estados = len(self.registro_estados) is 1
        es_pendiente = self.estado_actual == u'Pendiente'
        return cant_estados == 1 and es_pendiente
