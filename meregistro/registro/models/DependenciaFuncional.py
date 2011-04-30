from django.db import models
from meregistro.registro.models.Jurisdiccion import Jurisdiccion
from meregistro.registro.models.GestionJurisdiccion import GestionJurisdiccion
from meregistro.registro.models.TipoGestion import TipoGestion
from meregistro.registro.models.TipoDependenciaFuncional import TipoDependenciaFuncional
from meregistro.seguridad.models import Ambito

class DependenciaFuncional(models.Model):
	nombre = models.CharField(max_length = 50)
	jurisdiccion = models.ForeignKey(Jurisdiccion)
	gestion_jurisdiccion = models.ForeignKey(GestionJurisdiccion)
	tipo_gestion = models.ForeignKey(TipoGestion)
	tipo_dependencia_funcional = models.ForeignKey(TipoDependenciaFuncional)
	ambito = models.ForeignKey(Ambito, editable=False)

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

	def hasEstablecimientos(self):
		from meregistro.registro.models.Establecimiento import Establecimiento
		establecimientos = Establecimiento.objects.filter(dependencia_funcional = self)
		return establecimientos.count() > 0
