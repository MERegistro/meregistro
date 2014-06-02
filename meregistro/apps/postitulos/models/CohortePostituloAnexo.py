# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Anexo import Anexo
from apps.postitulos.models.CohortePostitulo import CohortePostitulo
from apps.postitulos.models.EstadoCohortePostituloAnexo import EstadoCohortePostituloAnexo
import datetime

"Cada asignación de una cohorte a un anexo"
class CohortePostituloAnexo(models.Model):
	anexo = models.ForeignKey(Anexo, related_name='cohortes_postitulo')
	cohorte_postitulo = models.ForeignKey(CohortePostitulo)
	inscriptos = models.PositiveIntegerField(null=True)
	estado = models.ForeignKey(EstadoCohortePostituloAnexo) # Concuerda con el último estado en CohorteEstablecimientoEstado
	
	class Meta:
		app_label = 'postitulos'
		ordering = ['cohorte__anio']
		db_table = 'postitulos_cohortes_postitulo_anexos'
		unique_together = ('anexo', 'cohorte_postitulo')


	def __unicode__(self):
		return str(self.anexo) + ' - ' + str(self.cohorte)


	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(CohortePostituloAnexo, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()


	"La cohorte fue aceptada por el anexo?"
	def registrada(self):
		return self.estado.nombre == EstadoCohortePostituloAnexo.REGISTRADA


	"La cohorte fue rechazada por el anexo?"
	def rechazada(self):
		return self.estado.nombre == EstadoCohortePostituloAnexo.RECHAZADA


	def registrar_estado(self):
		from apps.postitulos.models.CohortePostituloAnexoEstado import CohortePostituloAnexoEstado
		registro = CohortePostituloAnexoEstado(estado=self.estado)
		registro.fecha = datetime.date.today()
		registro.cohorte_anexo_id = self.id
		registro.save()


	def get_estados(self):
		from apps.titulos.models.CohortePostituloAnexoEstado import CohortePostituloAnexoEstado
		try:
			estados = CohortePostituloAnexoEstado.objects.filter(cohorte_anexo=self).order_by('fecha', 'id')
		except:
			estados = {}
		return estados > 0
	
	
	def is_editable(self):
		return self.registrada()
		
		
	def is_rechazable(self):
		return not self.rechazada() and self.inscriptos == None
		
		
	def get_establecimiento(self):
		return self.anexo.establecimiento
		
		
	def get_unidad_educativa(self):
		return self.anexo
