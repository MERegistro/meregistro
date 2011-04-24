from django.db import models
from meregistro.registro.models import Jurisdiccion, GestionJurisdiccion, TipoGestion, TipoDependenciaFuncional
from meregistro.seguridad.models import Ambito

class DependenciaFuncional(models.Model):
	nombre = models.CharField(max_length = 50)
	jurisdiccion = models.ForeignKey(Jurisdiccion)
	gestion_jurisdiccion = models.ForeignKey(GestionJurisdiccion)
	tipo_gestion = models.ForeignKey(TipoGestion)
	tipo_dependencia_funcional = models.ForeignKey(TipoDependenciaFuncional)
	ambito = models.ForeignKey(Ambito)

	class Meta:
		app_label = 'registro'
		ordering = ['nombre']

	def __unicode__(self):
		return self.nombre

	def save(self):
		self.updateAmbito()
		models.Model.save(self)

	def updateAmbito(self):
		if self.pk is None or self.ambito is None:
			self.ambito = self.jurisdiccion.ambito.createChild(self.nombre)
		else:
			self.ambito.descripcion = self.nombre
			self.ambito.save()
