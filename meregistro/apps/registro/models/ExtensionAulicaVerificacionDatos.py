# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.ExtensionAulica import ExtensionAulica


class ExtensionAulicaVerificacionDatos(models.Model):
    extension_aulica = models.OneToOneField(ExtensionAulica)
    datos_basicos = models.BooleanField()
    contacto = models.BooleanField()
    alcances = models.BooleanField()
    turnos = models.BooleanField()
    funciones = models.BooleanField()
    domicilios = models.BooleanField()
    autoridades = models.BooleanField()
    info_edilicia = models.BooleanField()
    conectividad = models.BooleanField()
    matricula = models.BooleanField()
    
    class Meta:
        app_label = 'registro'
        db_table = 'registro_extension_aulica_verificacion_datos'
        

    def completo(self):
        return (self.datos_basicos and self.contacto and self.alcances and self.turnos
            and self.funciones and self.domicilios and self.autoridades
            and self.info_edilicia and self.conectividad)


    def get_datos_verificados(self):
        return {
            'datos_basicos': self.datos_basicos, 
            'contacto': self.contacto, 
            'alcances': self.alcances, 
            'turnos': self.turnos, 
            'funciones': self.funciones, 
            'domicilios': self.domicilios, 
            'autoridades': self.autoridades,
            'info_edilicia': self.info_edilicia, 
            'conectividad': self.conectividad,
            'matricula': self.matricula
        }
