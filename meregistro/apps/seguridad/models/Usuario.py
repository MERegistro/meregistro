# -*- coding: UTF-8 -*-

from django.db import models
from apps.seguridad.models import TipoDocumento
from datetime import datetime
from apps.seguridad.audit import audit

@audit
class Usuario(models.Model):
    tipo_documento = models.ForeignKey(TipoDocumento)
    documento = models.CharField(max_length=8)
    apellido = models.CharField(max_length=40)
    nombre = models.CharField(max_length=40)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255, null=True, editable=False)
    last_login = models.DateTimeField(null=True, blank=True, editable=False)
    is_active = models.BooleanField(null=False, blank=False, editable=False)
    logins_count = models.IntegerField(null=True, blank=True, editable=False, default=0)

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

    def can_delete_perfil(self, perfil):
        """ TODO: Chequea (de alguna manera) que el usuario puede eliminar el perfil """
        return True

    def can_delete_usuario(self, usuario):
        """ Chequea (de alguna manera) que el usuario puede eliminar al usuario pasado como argumento """
        return True

    def update_last_login(self):
        self.logins_count += 1
        self.last_login = datetime.now()
        self.save()

    def is_deletable(self):
        nunca_logueado = self.last_login is None
        return nunca_logueado

    def perfiles_vigentes(self):
      return self.perfiles.filter(fecha_desasignacion=None)

    @classmethod
    def get_usuarios_by_rol(cls, rol):
        usuarios = Usuario.objects.filter(perfiles__rol__nombre=rol)
        return usuarios
