# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.postitulos.models.CohortePostitulo import CohortePostitulo
from apps.postitulos.models.EstadoCohortePostituloExtensionAulica import EstadoCohortePostituloExtensionAulica
import datetime

"Cada asignación de una cohorte a un anexo"
class CohortePostituloExtensionAulica(models.Model):
	extension_aulica = models.ForeignKey(ExtensionAulica, related_name='cohortes_postitulo')
	cohorte_postitulo = models.ForeignKey(CohortePostitulo)
	inscriptos = models.PositiveIntegerField(null=True)
	estado = models.ForeignKey(EstadoCohortePostituloExtensionAulica) # Concuerda con el último estado en CohorteExtensionAulicaEstado


	class Meta:
		app_label = 'postitulos'
		ordering = ['cohorte__anio']
		db_table = 'postitulos_cohortes_postitulo_extensiones_aulicas'
		unique_together = ('extension_aulica', 'cohorte_postitulo')


	def __unicode__(self):
		return str(self.extension_aulica) + ' - ' + str(self.cohorte)


	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(CohortePostituloExtensionAulica, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()


	"La cohorte fue aceptada por la extensión áulica?"
	def registrada(self):
		return self.estado.nombre == EstadoCohortePostituloExtensionAulica.REGISTRADA


	"La cohorte fue rechazada por la extensión áulica?"
	def rechazada(self):
		return self.estado.nombre == EstadoCohortePostituloExtensionAulica.RECHAZADA


	def registrar_estado(self):
		from apps.postitulos.models.CohortePostituloExtensionAulicaEstado import CohortePostituloExtensionAulicaEstado
		registro = CohortePostituloExtensionAulicaEstado(estado=self.estado)
		registro.fecha = datetime.date.today()
		registro.cohorte_positulo_extension_aulica_id = self.id
		registro.save()


	def get_estados(self):
		from apps.postitulos.models.CohortePostituloExtensionAulicaEstado import CohortePostituloExtensionAulicaEstado
		try:
			estados = CohortePostituloExtensionAulicaEstado.objects.filter(cohorte_postitulo_extension_aulica=self).order_by('fecha', 'id')
		except:
			estados = {}
		return estados
	
	
	def is_editable(self):
		return self.registrada()
			
		
	def is_rechazable(self):
		return not self.rechazada() and self.inscriptos == None

		
	def get_establecimiento(self):
		return self.extension_aulica.establecimiento

		
	def get_unidad_educativa(self):
		return self.extension_aulica
