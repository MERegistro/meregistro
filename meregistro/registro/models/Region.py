from django.db import models
from seguridad.models import Ambito

class Region(models.Model):
	nombre = models.CharField(max_length=50, unique=True)
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
			self.ambito = Ambito.objects.get(level=0).createChild(self.nombre)
		else:
			self.ambito.descripcion = self.nombre
			self.ambito.save()
    
