# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.EstadoTituloNacional import EstadoTituloNacional
from apps.titulos.models.NormativaNacional import NormativaNacional
from apps.titulos.models.Carrera import Carrera
import datetime


class TituloNacional(models.Model):
	nombre = models.CharField(max_length=200)
	normativa_nacional = models.ForeignKey(NormativaNacional)
	estado = models.ForeignKey(EstadoTituloNacional) # Concuerda con el último estado en TituloEstado
	observaciones = models.CharField(max_length=255, null=True, blank=True)
	fecha_alta = models.DateField(auto_now_add=True)
	carreras = models.ManyToManyField(Carrera, db_table='titulos_titulos_nacionales_carreras', related_name='titulos_asignados') # Carreras

	class Meta:
		app_label = 'titulos'
		ordering = ['nombre']
		db_table = 'titulos_titulo_nacional'
		unique_together = ('nombre', 'normativa_nacional')

	def __unicode__(self):
		return self.nombre

	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(TituloNacional, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()

	"Sobreescribo para eliminar los objetos relacionados"
	def delete(self, *args, **kwargs):
		for carrera in self.carreras.all():
			carrera.delete()
		for est in self.estados.all():
			est.delete()
		super(TituloNacional, self).delete(*args, **kwargs)

	def registrar_estado(self):
		from apps.titulos.models.TituloNacionalEstado import TituloNacionalEstado
		registro = TituloNacionalEstado(estado=self.estado)
		registro.fecha = datetime.date.today()
		registro.titulo_nacional_id = self.id
		registro.save()

	def get_estados(self):
		from apps.titulos.models.TituloNacionalEstado import TituloNacionalEstado
		try:
			estados = TituloNacionalEstado.objects.filter(titulo_nacional=self).order_by('fecha', 'id')
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
