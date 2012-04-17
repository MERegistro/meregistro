# -*- coding: UTF-8 -*-

from django.db import models
from apps.seguridad.models import Credencial, TipoAmbito


class Rol(models.Model):
    
    ROL_ADMIN_NACIONAL = 'AdminNacional'
    ROL_ADMIN_SEGURIDAD = 'AdminSeguridad'
    ROL_REFERENTE_JURISDICCIONAL = 'ReferenteJurisdiccional'
    ROL_REFERENTE_INSTITUCIONAL = 'ReferenteInstitucional'

    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=255)
    credenciales = models.ManyToManyField(Credencial, related_name='roles')
    tipos_ambito_asignable = models.ManyToManyField(TipoAmbito, related_name='roles')
    roles_asignables = models.ManyToManyField('self', related_name='roles_asignadores', symmetrical=False)
    path = models.CharField(max_length=255)
    padre = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        app_label = 'seguridad'

    def __unicode__(self):
        return self.descripcion


    def save(self):
        if self.padre is None:
            padre_path = '/'
        else:
            padre_path = self.padre.path
        self.path = padre_path + str(self.id) + '/'
        models.Model.save(self)


    def asigna(self, rol):
        return bool(self.roles_asignables.filter(id=rol.id))

    def asignableAAmbito(self, ambito):
        return bool(self.tipos_ambito_asignable.filter(id=ambito.tipo.id))
