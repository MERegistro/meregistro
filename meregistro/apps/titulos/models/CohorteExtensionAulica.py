# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.titulos.models.Cohorte import Cohorte
from apps.titulos.models.EstadoCohorteExtensionAulica import EstadoCohorteExtensionAulica
import datetime

"Cada asignación de una cohorte a un anexo"
class CohorteExtensionAulica(models.Model):
	extension_aulica = models.ForeignKey(ExtensionAulica, related_name='cohortes')
	cohorte = models.ForeignKey(Cohorte)
	oferta = models.NullBooleanField()
	inscriptos = models.PositiveIntegerField(null=True)
	estado = models.ForeignKey(EstadoCohorteExtensionAulica) # Concuerda con el último estado en CohorteExtensionAulicaEstado

	class Meta:
		app_label = 'titulos'
		ordering = ['cohorte__anio']
		db_table = 'titulos_cohortes_extensiones_aulicas'
		unique_together = ('extension_aulica', 'cohorte')

	def __unicode__(self):
		return str(self.extension_aulica) + ' - ' + str(self.cohorte)

	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(CohorteExtensionAulica, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()

	"La cohorte fue aceptada por la extensión áulica?"
	def registrada(self):
		return self.estado.nombre == EstadoCohorteExtensionAulica.REGISTRADA

	def registrar_estado(self):
		from apps.titulos.models.CohorteExtensionAulicaEstado import CohorteExtensionAulicaEstado
		registro = CohorteExtensionAulicaEstado(estado=self.estado)
		registro.fecha = datetime.date.today()
		registro.cohorte_extension_aulica_id = self.id
		registro.save()

	def get_estados(self):
		from apps.titulos.models.CohorteExtensionAulicaEstado import CohorteExtensionAulicaEstado
		try:
			estados = CohorteExtensionAulicaEstado.objects.filter(cohorte_extension_aulica=self).order_by('fecha', 'id')
		except:
			estados = {}
		return estados
