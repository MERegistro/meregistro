# -*- coding: utf-8 -*-
from django.db import models

class ConfiguracionSolapasExtensionAulica(models.Model):
  datos_basicos = models.BooleanField()
  contacto = models.BooleanField()
  alcances = models.BooleanField()
  turnos = models.BooleanField()
  funciones = models.BooleanField()
  domicilio = models.BooleanField()
  informacion_edilicia = models.BooleanField()
  conexion_internet = models.BooleanField()
  matricula = models.BooleanField()

  class Meta:
    app_label = 'seguridad'
    db_table = 'seguridad_configuracion_solapas_extension_aulica'

  @classmethod 
  def get_instance(cls):
    return ConfiguracionSolapasExtensionAulica.objects.get(pk=1)
