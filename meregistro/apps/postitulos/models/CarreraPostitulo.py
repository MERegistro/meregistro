# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Jurisdiccion import Jurisdiccion
from apps.postitulos.models.EstadoCarreraPostitulo import EstadoCarreraPostitulo

class CarreraPostitulo(models.Model):
	nombre = models.CharField(max_length=255)
	estado = models.ForeignKey(EstadoCarreraPostitulo) # Concuerda con el último estado en CarreraPostituloEstado
	jurisdicciones = models.ManyToManyField(Jurisdiccion, db_table='postitulos_carreras_postitulo_jurisdicciones')
	observaciones = models.CharField(max_length=255, null=True, blank=True)
	fecha_alta = models.DateField(auto_now_add=True)
	carrera_sin_orientacion = models.BooleanField()

	class Meta:
		app_label = 'postitulos'
		ordering = ['nombre']
        db_table = 'postitulos_carrera_postitulo'

	def __unicode__(self):
		return self.nombre
		
	def __init__(self, *args, **kwargs):
		super(CarreraPostitulo, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()

	def registrar_estado(self):
		import datetime
		from apps.postitulos.models.CarreraPostituloEstado import CarreraPostituloEstado
		registro = CarreraPostituloEstado(estado=self.estado)
		registro.fecha = datetime.date.today()
		registro.carrera_postitulo_id = self.id
		registro.save()

	def get_estados(self):
		from apps.postitulos.models.CarreraPostituloEstado import CarreraPostituloEstado
		try:
			estados = CarreraPostituloEstado.objects.filter(carrera_postitulo=self).order_by('fecha', 'id')
		except:
			estados = {}
		return estados
