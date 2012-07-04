# -*- coding: UTF-8 -*-

from django.db import models
from apps.seguridad.models import Usuario


class PasswordRememberKey(models.Model):
    usuario = models.ForeignKey(Usuario)
    key = models.CharField(max_length=255)

    class Meta:
        app_label = 'seguridad'
        db_table = 'seguridad_password_remember_key'
