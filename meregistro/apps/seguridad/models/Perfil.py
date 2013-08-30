# -*- coding: UTF-8 -*-

from django.db import models
from apps.seguridad.models import Ambito, Rol, Usuario
from apps.seguridad.audit import audit

@audit
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

	
	def can_modificar_usuario(self, usuario):
		if self.rol.path is None:
			return False
		cant_pefiles_visibles = len(
			usuario.perfiles.filter(ambito__path__istartswith=self.ambito.path)
			.filter(rol__path__istartswith=self.rol.path))
		return  cant_pefiles_visibles == len(usuario.perfiles.all()) or self.usuario.id == usuario.id


	def is_deletable(self):
		total = self.usuario.perfiles.filter(fecha_desasignacion=None).count()
		mas_de_uno = total > 1
		no_desasignado = self.fecha_desasignacion is None
		return mas_de_uno and no_desasignado


	def can_delete_perfil(self, perfil):
		return (self.ambito.esAncestro(perfil.ambito)
			and self.rol.asigna(perfil.rol))

	def __unicode__(self):
		return unicode(self.rol) + ' (' + unicode(self.ambito) + ')'
