# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models.Postitulo import Postitulo
from apps.postitulos.models.CarreraPostitulo import CarreraPostitulo
from apps.postitulos.models.EstadoCarreraPostituloJurisdiccional import EstadoCarreraPostituloJurisdiccional
from apps.postitulos.models.NormativaPostitulo import NormativaPostitulo
from apps.registro.models.Jurisdiccion import Jurisdiccion
import datetime

"""
Postítulo jurisdiccional
"""

class CarreraPostituloJurisdiccional(models.Model):
	carrera_postitulo = models.ForeignKey(CarreraPostitulo)
	normativas = models.ManyToManyField(NormativaPostitulo, db_table='postitulos_carreras_postitulos_normativas')
	jurisdiccion = models.ForeignKey(Jurisdiccion)
	estado = models.ForeignKey(EstadoCarreraPostituloJurisdiccional)
	revisado_jurisdiccion = models.NullBooleanField(default=False, null=True)

	class Meta:
		app_label = 'postitulos'
		unique_together = ('carrera_postitulo', 'jurisdiccion')
		db_table = 'postitulos_carrera_postitulo_jurisdiccional'
		ordering = ['id']

	def __unicode__(self):
		return self.carrera_postitulo.nombre

	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(CarreraPostituloJurisdiccional, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()

	"Sobreescribo para eliminar lo objetos relacionados"
	"""
	def delete(self, *args, **kwargs):
		for est in self.estados:
			est.delete()
		try:
			self.modalidad_presencial.delete()
			self.modalidad_distancia.delete()
		except:
			pass
		super(CarreraJurisdiccional, self).delete(*args, **kwargs)



	"Se eliminan las orientaciones, por ejemplo al cambiar el título"
	def eliminar_orientaciones(self):
		#for orientacion in self.orientaciones.all():
		#	orientacion.delete()
		pass	
	"""

	def registrar_estado(self):
		from apps.postitulos.models.CarreraPostituloJurisdiccionalEstado import CarreraPostituloJurisdiccionalEstado
		registro = CarreraPostituloJurisdiccionalEstado(estado=self.estado)
		registro.fecha = datetime.date.today()
		registro.carrera_postitulo_jurisdiccional = self
		registro.save()

	def get_estados(self):
		from apps.postitulos.models.CarreraPostituloJurisdiccionalEstado import CarreraPostituloJurisdiccionalEstado
		try:
			estados = CarreraPostituloJurisdiccionalEstado.objects.filter(carrera_postitulo_jurisdiccional=self).order_by('fecha', 'id')
		except:
			estados = {}
		return estados

	def getEstadoActual(self):
		try:
			return list(self.estados)[-1].estado
		except IndexError:
			return None

	def controlada(self):
		return self.estado.nombre == EstadoCarreraPostituloJurisdiccional.CONTROLADA
