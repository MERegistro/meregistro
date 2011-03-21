# -*- coding: UTF-8 -*-

from django.db import models
from meregistro.seguridad.models import TipoDocumento

class Usuario(models.Model):
  tipo_documento = models.ForeignKey(TipoDocumento)
  documento = models.CharField(max_length=20)
  apellido = models.CharField(max_length=40)
  nombre = models.CharField(max_length=40)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255, null=True, editable=False)
  last_login = models.IntegerField(null=True, blank=True, editable=False)
  
  def set_password(self, password):
    from seguridad.authenticate import encrypt_password
    self.password = encrypt_password(self, password)
  
  class Meta:
    app_label = 'seguridad'
    unique_together = ("tipo_documento", "documento")

  def is_anonymous(self):
    return self.id is None
  
  def is_authenticated(self):
    return self.id is not None
