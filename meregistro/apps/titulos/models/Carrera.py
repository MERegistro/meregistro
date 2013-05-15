# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Jurisdiccion import Jurisdiccion
from apps.titulos.models.EstadoCarrera import EstadoCarrera

class Carrera(models.Model):
	nombre = models.CharField(max_length=50, unique=True)
	estado = models.ForeignKey(EstadoCarrera) # Concuerda con el último estado en CarreraEstado
	jurisdicciones = models.ManyToManyField(Jurisdiccion, db_table='titulos_carreras_jurisdicciones') # Provincias
	observaciones = models.CharField(max_length=255, null=True, blank=True)
	fecha_alta = models.DateField(auto_now_add=True)

	class Meta:
		app_label = 'titulos'
		ordering = ['nombre']

	def __unicode__(self):
		return self.nombre
		
	def __init__(self, *args, **kwargs):
		super(Carrera, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()

	def registrar_estado(self):
		import datetime
		from apps.titulos.models.CarreraEstado import CarreraEstado
		registro = CarreraEstado(estado=self.estado)
		registro.fecha = datetime.date.today()
		registro.carrera_id = self.id
		registro.save()

	def get_estados(self):
		from apps.titulos.models.CarreraEstado import CarreraEstado
		try:
			estados = CarreraEstado.objects.filter(carrera=self).order_by('fecha', 'id')
		except:
			estados = {}
		return estados
		
		
	#def carrera_jurisdiccional(self):
	#	tmp = False
	#	return tmp
