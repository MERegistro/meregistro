# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.EstadoNormativaNacional import EstadoNormativaNacional
import datetime

class NormativaNacional(models.Model):
	numero = models.CharField(max_length=50, unique=True)
	descripcion = models.CharField(max_length=255)
	observaciones = models.CharField(max_length=255, null=True, blank=True)
	estado = models.ForeignKey(EstadoNormativaNacional) # Concuerda con el último estado en NormativaNacionalEstado
	fecha_alta = models.DateField(auto_now_add=True)

	class Meta:
		app_label = 'titulos'
		db_table = 'titulos_normativa_nacional'

	def __unicode__(self):
		return str(self.numero)


	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(NormativaNacional, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()


	def registrar_estado(self):
		import datetime
		from apps.titulos.models.NormativaNacionalEstado import NormativaNacionalEstado
		registro = NormativaNacionalEstado(estado=self.estado)
		registro.fecha = datetime.date.today()
		registro.normativa_nacional_id = self.id
		registro.save()

	def get_estados(self):
		from apps.titulos.models.NormativaNacionalEstado import NormativaNacionalEstado
		try:
			estados = NormativaNacionalEstado.objects.filter(normativa_nacional=self).order_by('fecha', 'id')
		except:
			estados = {}
		return estados


	"Algún título nacional está asociado a la normativa?"
	def asociada_titulo(self):
		from apps.titulos.models.Titulo import Titulo
		return False
		#return Titulo.objects.filter(normativa_nacional__id=self.id).exists() # Por ahora no existe esta relación
	
	"Eliminable?"
	def is_deletable(self):
		ret = self.asociada_titulo() == False
		return ret
