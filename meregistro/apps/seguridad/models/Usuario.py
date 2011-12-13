# -*- coding: UTF-8 -*-

from django.db import models
from apps.seguridad.models import TipoDocumento
from datetime import datetime


class Usuario(models.Model):
    tipo_documento = models.ForeignKey(TipoDocumento)
    documento = models.CharField(max_length=20)
    apellido = models.CharField(max_length=40)
    nombre = models.CharField(max_length=40)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255, null=True, editable=False)
    last_login = models.IntegerField(null=True, blank=True, editable=False)
    is_active = models.BooleanField(null=False, blank=False, editable=False)

    class Meta:
        app_label = 'seguridad'
        unique_together = ("tipo_documento", "documento")

    def set_password(self, password):
        from apps.seguridad.authenticate import encrypt_password
        self.password = encrypt_password(password)

    def is_anonymous(self):
        return self.id is None

    def is_authenticated(self):
        return self.id is not None

    def lock(self, motivo):
        """ Inhabilitar al usuario """
        self.__set_lock(False, motivo)

    def unlock(self, motivo):
        """ Habilitar al usuario """
        self.__set_lock(True, motivo)

    def __set_lock(self, is_active, motivo):
        """ Registra un bloqueo/desbloqueo y su motivo """
        from apps.seguridad.models import BloqueoLog
        self.is_active = is_active
        self.save()
        log = BloqueoLog(usuario=self, motivo=motivo, fecha=datetime.now())
        log.save()

    def asignarPerfil(self, rol, ambito, fechaAsignacion):
        """ Asigna al usuario un perfil """
        from apps.seguridad.models import Rol, Ambito, Perfil
        perfil = Perfil(usuario=self, rol=rol, ambito=ambito, fecha_asignacion=fechaAsignacion)
        perfil.save()
