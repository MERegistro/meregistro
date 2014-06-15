# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models.EstadoPostituloNacional import EstadoPostituloNacional
from apps.postitulos.models.NormativaPostitulo import NormativaPostitulo
from apps.postitulos.models.CarreraPostitulo import CarreraPostitulo
import datetime


class PostituloNacional(models.Model):
	nombre = models.CharField(max_length=255)
	normativa_postitulo = models.ForeignKey(NormativaPostitulo)
	estado = models.ForeignKey(EstadoPostituloNacional) # Concuerda con el último estado en TituloEstado
	observaciones = models.CharField(max_length=255, null=True, blank=True)
	fecha_alta = models.DateField(auto_now_add=True)
	carreras = models.ManyToManyField(CarreraPostitulo, db_table='postitulos_postitulos_nacionales_carreras', related_name='postitulos_asignados') # Carreras

	class Meta:
		app_label = 'postitulos'
		ordering = ['nombre']
		db_table = 'postitulos_postitulo_nacional'
		unique_together = ('nombre', 'normativa_postitulo')

	def __unicode__(self):
		return self.nombre

	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(PostituloNacional, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()

	"Sobreescribo para eliminar los objetos relacionados"
	def delete(self, *args, **kwargs):
		for carrera in self.carreras.all():
			carrera.delete()
		for est in self.estados.all():
			est.delete()
		super(PostituloNacional, self).delete(*args, **kwargs)

	def registrar_estado(self):
		from apps.postitulos.models.PostituloNacionalEstado import PostituloNacionalEstado
		registro = PostituloNacionalEstado(estado=self.estado)
		registro.fecha = datetime.date.today()
		registro.postitulo_nacional_id = self.id
		registro.save()

	def get_estados(self):
		from apps.postitulos.models.PostituloNacionalEstado import PostituloNacionalEstado
		try:
			estados = PostituloNacionalEstado.objects.filter(postitulo_nacional=self).order_by('fecha', 'id')
		except:
			estados = {}
		return estados

	"Alguna carrera asociada?"
	def asociado_carrera(self):
		ret = True
		try:
			test = self.carreras.all()[0]
		except IndexError:
			ret = False
		return ret 
	
	"Eliminable?"
	def is_deletable(self):
		ret = self.asociado_carrera() == False
		return ret
