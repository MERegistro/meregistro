from django.db import models
from meregistro.registro.models import Region
from meregistro.seguridad.models import Ambito

class Jurisdiccion(models.Model):
	prefijo = models.IntegerField(null = True)
	region = models.ForeignKey(Region)
	nombre = models.CharField(max_length=50)
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
			self.ambito = self.region.ambito.createChild(self.nombre)
		else:
			self.ambito.descripcion = self.nombre
			self.ambito.save()
