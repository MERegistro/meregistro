from django.db import models

class TipoDomicilio(models.Model):
	descripcion = models.CharField(max_length = 50, unique = True)

	class Meta:
		app_label = 'registro'
		db_table = 'registro_tipo_domicilio'
		ordering = ['descripcion']

	def __unicode__(self):
		return self.descripcion
