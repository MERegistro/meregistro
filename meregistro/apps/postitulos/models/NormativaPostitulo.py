# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models.EstadoNormativaPostitulo import EstadoNormativaPostitulo
import datetime

class NormativaPostitulo(models.Model):
	numero = models.CharField(max_length=50, unique=True)
	descripcion = models.CharField(max_length=255)
	observaciones = models.CharField(max_length=255, null=True, blank=True)
	estado = models.ForeignKey(EstadoNormativaPostitulo) # Concuerda con el último estado en NormativaNacionalEstado
	fecha_alta = models.DateField(auto_now_add=True)

	class Meta:
		app_label = 'postitulos'
		db_table = 'postitulos_normativa'

	def __unicode__(self):
		return str(self.numero)


	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(NormativaPostitulo, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()


	def registrar_estado(self):
		import datetime
		from apps.postitulos.models.NormativaPostituloEstado import NormativaPostituloEstado
		registro = NormativaPostituloEstado(estado=self.estado)
		registro.fecha = datetime.date.today()
		registro.normativa_postitulo_id = self.id
		registro.save()

	def get_estados(self):
		from apps.postitulos.models.NormativaPostituloEstado import NormativaPostituloEstado
		try:
			estados = NormativaPostituloEstado.objects.filter(normativa_postitulo=self).order_by('fecha', 'id')
		except:
			estados = {}
		return estados

	"Algún postítulo nacional está asociado a la normativa?"
	def asociada_postitulo_nacional(self):
		from apps.postitulos.models.PostituloNacional import PostituloNacional
		return PostituloNacional.objects.filter(normativa_postitulo__id=self.id).exists()
	
	"Eliminable?"
	def is_deletable(self):
		ret = self.asociada_postitulo_nacional() == False
		return ret
