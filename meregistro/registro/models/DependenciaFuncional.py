from django.db import models
from meregistro.registro.models import Jurisdiccion, GestionJurisdiccion, TipoGestion, TipoDependenciaFuncional

class DependenciaFuncional(models.Model):
	nombre = models.CharField(max_length = 50)
	jurisdiccion = models.ForeignKey(Jurisdiccion)
	gestion_jurisdiccion = models.ForeignKey(GestionJurisdiccion)
	tipo_gestion = models.ForeignKey(TipoGestion)
	tipo_dependencia_funcional = models.ForeignKey(TipoDependenciaFuncional)

	class Meta:
		app_label = 'registro'
		ordering = ['nombre']

	def __unicode__(self):
		return self.nombre
