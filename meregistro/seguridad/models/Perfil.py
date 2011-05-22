# -*- coding: UTF-8 -*-

from django.db import models
from meregistro.seguridad.models import Ambito, Rol, Usuario


class Perfil(models.Model):
    suario = models.ForeignKey(Usuario, related_name='perfiles')
    mbito = models.ForeignKey(Ambito)
    ol = models.ForeignKey(Rol)
    echa_asignacion = models.DateField()
    echa_desasignacion = models.DateField(null=True, blank=True)

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
