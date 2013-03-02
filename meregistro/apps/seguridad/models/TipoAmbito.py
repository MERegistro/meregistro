# -*- coding: UTF-8 -*-

from django.db import models

class TipoAmbito(models.Model):
	TIPO_SEDE = 'Sede'
	TIPO_ANEXO = 'Anexo'
	TIPO_EXTENSION_AULICA = 'ExtensionAulica'
	TIPO_JURISDICCION = 'Jurisdiccion'
	TIPO_DEPENDENCIA_FUNCIONAL = 'DependenciaFuncional'
	
	nombre = models.CharField(max_length=40)
	descripcion = models.CharField(max_length=100)

	class Meta:
		app_label = 'seguridad'

	def __unicode__(self):
		return self.descripcion

	@staticmethod
	def get_tipo_by_model(model):
		tipo_modelo = {'Establecimiento': 'Sede',
			'Anexo': 'Anexo',
			'ExtensionAulica': 'ExtensionAulica',
			'Jurisdiccion': 'Jurisdiccion',
			'DependenciaFuncional': 'DependenciaFuncional'
		}
		print model.__class__.__name__
		return TipoAmbito.objects.get(nombre=tipo_modelo[model.__class__.__name__])
