from django.db import models

class Estado(models.Model):

	PENDIENTE = 'Pendiente'
	BAJA = 'Baja'
	REGISTRADO = 'Registrado'
	NO_VIGENTE = 'No vigente'
	VIGENTE = 'Vigente'

	nombre = models.CharField(max_length = 50, unique = True)

	class Meta:
		app_label = 'registro'
		ordering = ['nombre']

	def __unicode__(self):
		return self.nombre
