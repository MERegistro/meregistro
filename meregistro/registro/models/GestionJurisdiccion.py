from django.db import models

class GestionJurisdiccion(models.Model):
	nombre = models.CharField(max_length=50, unique=True)

	class Meta:
		app_label = 'registro'
		db_table = 'registro_gestion_jurisdiccion'
		ordering = ['nombre']

	def __unicode__(self):
		return self.nombre
