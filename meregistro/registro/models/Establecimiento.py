# -*- coding: utf-8 -*-
from django.db import models
from meregistro.registro.models.TipoNormativa import TipoNormativa
from meregistro.registro.models.Jurisdiccion import Jurisdiccion
from meregistro.registro.models.RegistroEstablecimiento import RegistroEstablecimiento
from meregistro.registro.models.DependenciaFuncional import DependenciaFuncional
from meregistro.registro.models.Estado import Estado
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import datetime
from meregistro.seguridad.models import Ambito

YEARS_CHOICES = tuple((int(n), str(n)) for n in range(1800, datetime.datetime.now().year + 1))


class Establecimiento(models.Model):
	dependencia_funcional = models.ForeignKey(DependenciaFuncional)
	cue = models.CharField(max_length = 5)
	nombre = models.CharField(max_length = 255)
	tipo_normativa = models.ForeignKey(TipoNormativa)
	unidad_academica = models.BooleanField()
	nombre_unidad_academica = models.CharField(max_length = 100, null = True, blank = True)
	norma_creacion = models.CharField(max_length = 100)
	observaciones = models.TextField(max_length = 255, null = True, blank = True)
	anio_creacion = models.IntegerField(null = True, blank = True, choices = YEARS_CHOICES)
	telefono = models.CharField(max_length = 100, null = True, blank = True)
	email = models.EmailField(max_length = 255, null = True, blank = True)
	sitio_web = models.URLField(max_length = 255, null = True, blank = True, verify_exists = False)
	ambito = models.ForeignKey(Ambito, editable = False, null=True)

	class Meta:
		app_label = 'registro'
		ordering = ['nombre']

	"""
	Sobreescribo el init para agregarle propiedades
	"""
	def __init__(self, *args, **kwargs):
		super(Establecimiento, self).__init__(*args, **kwargs)
		self.registro_estados = RegistroEstablecimiento.objects.filter(establecimiento = self).order_by('id')
		self.estado_actual = self.getEstadoActual()

	def __unicode__(self):
		return self.nombre

	def clean(self):
		#Chequea que la combinación entre jurisdiccion y cue sea única
		try:
			est = Establecimiento.objects.get(cue = self.cue, dependencia_funcional__jurisdiccion__id = self.dependencia_funcional.jurisdiccion.id)
			if est and est != self:
				raise ValidationError('Ya existe un establecimiento con ese CUE en su jurisdicción.')
		except ObjectDoesNotExist:
			pass

	def registrar_estado(self, estado):
		registro = RegistroEstablecimiento(estado = estado)
		registro.fecha_solicitud = datetime.date.today()
		registro.establecimiento_id = self.id
		registro.save()

	def save(self):
		self.updateAmbito()
		models.Model.save(self)

	def delete(self):
		estado = Estado.objects.get(nombre = Estado.BAJA)
		self.registrar_estado(estado)

	def updateAmbito(self):
		if self.pk is None or self.ambito is None:
			try:
				self.ambito = self.dependencia_funcional.ambito.createChild(self.nombre)
			except Exception:
				pass
		else:
			self.ambito.descripcion = self.nombre
			self.ambito.save()

	def hasAnexos(self):
		from meregistro.registro.models.Anexo import Anexo
		anexos = Anexo.objects.filter(establecimiento = self)
		return anexos.count() > 0

	def getEstadoActual(self):
		try:
			estado_actual = str(list(self.registro_estados)[-1])
		except IndexError:
			estado_actual = u''
		return estado_actual
	"""
	Se puede eliminar cuando:
	 * Tiene un sólo estado y es pendiente (hoy día si tiene un sólo estado ES pendiente)
	"""
	def isDeletable(self):
		cant_estados = len(self.registro_estados) is 1
		es_pendiente = self.estado_actual == u'Pendiente'
		return cant_estados == 1 and es_pendiente
