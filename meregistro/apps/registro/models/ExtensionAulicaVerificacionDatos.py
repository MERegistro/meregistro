# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.ExtensionAulica import ExtensionAulica


class ExtensionAulicaVerificacionDatos(models.Model):
    extension_aulica = models.OneToOneField(ExtensionAulica)
    datos_basicos = models.BooleanField()
    contacto = models.BooleanField()
    niveles = models.BooleanField()
    turnos = models.BooleanField()
    funciones = models.BooleanField()
    domicilios = models.BooleanField()
    #autoridades = models.BooleanField()
    info_edilicia = models.BooleanField()
    conectividad = models.BooleanField()
    #completo = models.BooleanField()

    class Meta:
        app_label = 'registro'
        db_table = 'registro_extension_aulica_verificacion_datos'

    def completo(self):
        return (self.datos_basicos and self.contacto and self.niveles and self.turnos
            and self.funciones and self.domicilios
            and self.info_edilicia and self.conectividad)
