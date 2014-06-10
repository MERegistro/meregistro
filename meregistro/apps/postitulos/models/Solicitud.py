# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models import Jurisdiccion
from apps.postitulos.models import CarreraPostitulo, PostituloNacional, EstadoPostituloNacional, NormativaPostituloJurisdiccional
from apps.postitulos.models.EstadoSolicitud import EstadoSolicitud
import datetime

"""
Solicitud de validez de Título nacional
"""
class Solicitud(models.Model):
	jurisdiccion = models.ForeignKey(Jurisdiccion, null=False, related_name="solicitudes_postitulo")
	carrera_postitulo = models.ForeignKey(CarreraPostitulo, null=False)
	postitulo_nacional = models.ForeignKey(PostituloNacional, null=False)
	primera_cohorte = models.PositiveIntegerField(null=True)
	ultima_cohorte = models.PositiveIntegerField(null=True)
	nro_expediente = models.CharField(max_length=200, null=True)
	normativas_jurisdiccionales = models.ManyToManyField(NormativaPostituloJurisdiccional, db_table='postitulos_solicitud_normativas_jurisdiccionales')
	normativas_postitulo = models.CharField(max_length=99, null=True)
	estado = models.ForeignKey(EstadoSolicitud, null=False, related_name="estados_postitulo") # Concuerda con el último estado en SolicitudEstado
	
	class Meta:
		app_label = 'postitulos'

	def __unicode__(self):
		return self.postitulo_nacional.nombre

	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(Solicitud, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()

	"Sobreescribo para eliminar los objetos relacionados"
	def delete(self, *args, **kwargs):
		for normativa in self.normativas_jurisdiccionales.all():
			normativa.delete()
		for est in self.estados.all():
			est.delete()
		super(Solicitud, self).delete(*args, **kwargs)

	def registrar_estado(self):
		from apps.postitulos.models import SolicitudEstado
		registro = SolicitudEstado(estado=self.estado)
		registro.fecha = datetime.date.today()
		registro.solicitud_id = self.id
		registro.save()

	def get_estados(self):
		from apps.postitulos.models import SolicitudEstado
		try:
			estados = SolicitudEstado.objects.filter(solicitud=self).order_by('fecha', 'id')
		except:
			estados = {}
		return estados

	def get_cues(self):
		return {}

	"""
	Asocia/elimina los establecimientos desde el formulario masivo
	XXX: los valores "posts" vienen como strings
	"""
	def save_establecimientos(self, establecimientos_procesados_ids, current_establecimientos_ids, establecimientos_seleccionados_ids):
		from apps.postitulos.models import SolicitudEstablecimiento
		
		"Borrar los que se des-chequean"
		for est_id in establecimientos_procesados_ids:
			if (str(est_id) not in establecimientos_seleccionados_ids) \
				and (est_id in current_establecimientos_ids): 
				# Si no está en los ids de la página, borrarlo
				SolicitudEstablecimiento.objects.get(solicitud__id=self.id, establecimiento=est_id).delete()

		"Agregar los nuevos"
		for est_id in establecimientos_seleccionados_ids:
			if int(est_id) not in current_establecimientos_ids:
				# Lo creo y registro el estado
				registro = SolicitudEstablecimiento.objects.create(solicitud=self, establecimiento_id=est_id)


	"""
	Asocia/elimina los establecimientos desde el formulario masivo
	XXX: los valores "posts" vienen como strings
	"""
	def save_anexos(self, anexos_procesados_ids, current_anexos_ids, anexos_seleccionados_ids):
		
		from apps.postitulos.models import SolicitudAnexo
		
		"Borrar los que se des-chequean"
		for est_id in anexos_procesados_ids:
			if (str(est_id) not in anexos_seleccionados_ids) and (est_id in current_anexos_ids): # Si no está en los ids de la página, borrarlo
				SolicitudAnexo.objects.get(solicitud__id=self.id, anexo=est_id).delete()

		"Agregar los nuevos"
		for est_id in anexos_seleccionados_ids:
			if int(est_id) not in current_anexos_ids:
				# Lo creo y registro el estado
				registro = SolicitudAnexo.objects.create(solicitud=self, anexo_id=est_id)


	def is_deletable(self):
		return self.estado.nombre == EstadoSolicitud.PENDIENTE
		
	
	def is_numerable(self):
		numerable = self.estado.nombre == EstadoSolicitud.CONTROLADO
		numerable = numerable and (len(self.establecimientos_postitulo.all()) > 0 or len(self.anexos_postitulo.all()) > 0)
		numerable = numerable and self.jurisdiccion and self.carrera_postitulo and self.primera_cohorte \
			and self.ultima_cohorte and len(self.normativas_jurisdiccionales.all()) > 0 and self.normativas_postitulo

		return numerable

		
	def numerado(self):
		return self.estado.nombre == EstadoSolicitud.NUMERADO

