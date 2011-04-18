from django.db import models
from meregistro.registro.models import Region

class Jurisdiccion(models.Model):
	prefijo = models.IntegerField(null = True)
	region = models.ForeignKey(Region)
	nombre = models.CharField(max_length=50)

	class Meta:
		app_label = 'registro'
		ordering = ['nombre']

	def __unicode__(self):
		return self.nombre
