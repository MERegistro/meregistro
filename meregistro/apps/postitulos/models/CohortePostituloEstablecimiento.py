# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.postitulos.models.CohortePostitulo import CohortePostitulo
from apps.postitulos.models.EstadoCohortePostituloEstablecimiento import EstadoCohortePostituloEstablecimiento
import datetime
	
"Cada asignación de una cohorte a un establecimiento"
class CohortePostituloEstablecimiento(models.Model):
	establecimiento = models.ForeignKey(Establecimiento, related_name='cohortes_postitulo')
	cohorte_postitulo = models.ForeignKey(CohortePostitulo)
	inscriptos = models.PositiveIntegerField(null=True)
	estado = models.ForeignKey(EstadoCohortePostituloEstablecimiento) # Concuerda con el último estado en CohorteEstablecimientoEstado

	class Meta:
		app_label = 'postitulos'
		ordering = ['cohorte__anio']
		db_table = 'postitulos_cohortes_postitulo_establecimientos'
		unique_together = ('establecimiento', 'cohorte_postitulo')


	def __unicode__(self):
		return str(self.establecimiento) + ' - ' + str(self.cohorte)


	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(CohortePostituloEstablecimiento, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()


	"La cohorte fue aceptada por el establecimiento?"
	def registrada(self):
		return self.estado.nombre == EstadoCohortePostituloEstablecimiento.REGISTRADA

	"La cohorte fue rechazada por el establecimiento?"
	def rechazada(self):
		return self.estado.nombre == EstadoCohortePostituloEstablecimiento.RECHAZADA


	def registrar_estado(self):
		from apps.postitulos.models.CohortePostituloEstablecimientoEstado import CohortePostituloEstablecimientoEstado
		registro = CohortePostituloEstablecimientoEstado(estado=self.estado)
		registro.fecha = datetime.date.today()
		registro.cohorte_establecimiento_id = self.id
		registro.save()


	def get_estados(self):
		from apps.postitulos.models.CohortePostituloEstablecimientoEstado import CohortePostituloEstablecimientoEstado
		try:
			estados = CohortePostituloEstablecimientoEstado.objects.filter(cohorte_postitulo_establecimiento=self).order_by('fecha', 'id')
		except:
			estados = {}
		return estados
	
	
	def is_editable(self):
		return self.registrada()
		
		
	def is_rechazable(self):
		return not self.rechazada() and self.inscriptos == None

		
	def get_establecimiento(self):
		return self.establecimiento

		
	def get_unidad_educativa(self):
		return self.establecimiento
