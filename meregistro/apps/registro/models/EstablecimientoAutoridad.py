# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.seguridad.models.TipoDocumento import TipoDocumento
from apps.registro.models.AutoridadCargo import AutoridadCargo
from django.core.exceptions import ValidationError


class EstablecimientoAutoridad(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, editable=False, related_name='autoridades')
    apellido = models.CharField(max_length=40, null=False)
    nombre = models.CharField(max_length=40, null=False)
    fecha_nacimiento = models.DateField(null=True)
    cargo = models.ForeignKey(AutoridadCargo, null=True, blank=True)
    tipo_documento = models.ForeignKey(TipoDocumento, null=True, blank=True)
    documento = models.CharField(max_length=8, null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    celular = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'registro'
        db_table = 'registro_establecimiento_autoridades'

    def __unicode__(self):
        return self.cargo.descripcion + ": " + self.apellido + " " + self.nombre

    def __init__(self, *args, **kwargs):
        super(EstablecimientoAutoridad, self).__init__(*args, **kwargs)
