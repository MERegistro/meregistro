# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.Titulo import Titulo
from apps.titulos.models.Carrera import Carrera
from apps.titulos.models.TipoTitulo import TipoTitulo
from apps.titulos.models.TituloOrientacion import TituloOrientacion
from apps.titulos.models.EstadoCarreraJurisdiccional import EstadoCarreraJurisdiccional
from apps.titulos.models.NormativaJurisdiccional import NormativaJurisdiccional
from apps.registro.models.Jurisdiccion import Jurisdiccion
import datetime

"""
Título jurisdiccional
"""

class CarreraJurisdiccional(models.Model):
	carrera = models.ForeignKey(Carrera)
	normativas = models.ManyToManyField(NormativaJurisdiccional, db_table='titulos_carreras_jurisdiccionales_normativas')
	jurisdiccion = models.ForeignKey(Jurisdiccion)
	estado = models.ForeignKey(EstadoCarreraJurisdiccional) # Concuerda con el último estado en TituloEstado
	revisado_jurisdiccion = models.NullBooleanField(default=False, null=True)

	class Meta:
		app_label = 'titulos'
		unique_together = ('carrera', 'jurisdiccion')
		db_table = 'titulos_carrera_jurisdiccional'
		ordering = ['id']

	def __unicode__(self):
		return self.carrera.nombre

	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(CarreraJurisdiccional, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()

	"Sobreescribo para eliminar lo objetos relacionados"
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

	def registrar_estado(self):
		from apps.titulos.models.CarreraJurisdiccionalEstado import CarreraJurisdiccionalEstado
		registro = CarreraJurisdiccionalEstado(estado = self.estado)
		registro.fecha = datetime.date.today()
		registro.carrera_jurisdiccional = self
		registro.save()

	def get_estados(self):
		from apps.titulos.models.CarreraJurisdiccionalEstado import CarreraJurisdiccionalEstado
		try:
			estados = CarreraJurisdiccionalEstado.objects.filter(carrera_jurisdiccional=self).order_by('fecha', 'id')
		except:
			estados = {}
		return estados

	def getEstadoActual(self):
		try:
			return list(self.estados)[-1].estado
		except IndexError:
			return None

	def controlada(self):
		return self.estado.nombre == EstadoCarreraJurisdiccional.CONTROLADA
		
	def tiene_cohortes_generadas(self):
		return self.datos_cohorte.exists()
	
