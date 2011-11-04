# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.EstadoAnexo import EstadoAnexo
from apps.registro.models.Turno import Turno
from apps.registro.models.Nivel import Nivel
from apps.registro.models.Funcion import Funcion
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from apps.seguridad.models import Ambito
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
    estado = models.ForeignKey(EstadoAnexo) # Concuerda con el último estado en AnexoEstado
    ambito = models.ForeignKey(Ambito, editable = False, null = True)
    revisado_jurisdiccion = models.NullBooleanField(default=False, null=True)
    niveles = models.ManyToManyField(Nivel, blank = True, null = True, db_table = 'registro_anexos_niveles')
    funciones = models.ManyToManyField(Funcion, blank = True, null = True, db_table = 'registro_anexos_funciones')

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

    def registrar_estado(self):
        from apps.registro.models.AnexoEstado import AnexoEstado
        registro = AnexoEstado(estado = self.estado)
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
        if self.id is not None:
            return self.estado
        else:
            return None

    def dadoDeBaja(self):
        return self.estado.nombre == EstadoAnexo.BAJA

    def save(self):
        self.updateAmbito()
        self.ambito.vigente = True
        self.ambito.save()
        models.Model.save(self)

    def updateAmbito(self):
        if self.pk is None or self.ambito is None:
            try:
                self.ambito = self.establecimiento.ambito.createChild(self.nombre)
            except Exception:
                pass
        else:
            self.ambito.descripcion = self.nombre
            self.ambito.save()

