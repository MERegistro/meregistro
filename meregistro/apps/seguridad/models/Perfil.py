# -*- coding: UTF-8 -*-

from django.db import models
from apps.seguridad.models import Ambito, Rol, Usuario


class Perfil(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='perfiles')
    ambito = models.ForeignKey(Ambito)
    rol = models.ForeignKey(Rol)
    fecha_asignacion = models.DateField()
    fecha_desasignacion = models.DateField(null=True, blank=True)

    class Meta:
        app_label = 'seguridad'

    def jurisdiccion(self):
        jurisdiccion = None
        ambito = self.ambito
        while jurisdiccion is None and ambito is not None:
            if ambito.jurisdiccion_set.count() > 0:
                jurisdiccion = ambito.jurisdiccion_set.all()[0]
            ambito = ambito.parent
        return jurisdiccion
    
    def ve_usuario(self, usuario):
        q = usuario.perfiles.filter(ambito__path__istartswith=self.ambito.path)
        return len(q) > 0
