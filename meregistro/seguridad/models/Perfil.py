# -*- coding: UTF-8 -*-

from django.db import models
from meregistro.seguridad.models import Ambito, Rol, Usuario

class Perfil(models.Model):
  usuario = models.ForeignKey(Usuario, related_name='perfiles')
  ambito = models.ForeignKey(Ambito)
  rol = models.ForeignKey(Rol)
  fecha_asignacion = models.DateField()
  fecha_desasignacion = models.DateField(null=True, blank=True)
  
  class Meta:
    app_label = 'seguridad'
