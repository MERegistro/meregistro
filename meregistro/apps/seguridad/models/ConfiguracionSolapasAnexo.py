# -*- coding: utf-8 -*-
from django.db import models

class ConfiguracionSolapasAnexo(models.Model):
  datos_basicos = models.BooleanField()
  contacto = models.BooleanField()
  alcances = models.BooleanField()
  turnos = models.BooleanField()
  funciones = models.BooleanField()
  domicilio = models.BooleanField()
  autoridad = models.BooleanField()
  informacion_edilicia = models.BooleanField()
  conexion_internet = models.BooleanField()
  matricula = models.BooleanField()

  class Meta:
    app_label = 'seguridad'
    db_table = 'seguridad_configuracion_solapas_anexo'

  @classmethod 
  def get_instance(cls):
    return ConfiguracionSolapasAnexo.objects.get(pk=1)
