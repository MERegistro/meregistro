from django.db import models

class TipoConexion(models.Model):
	nombre = models.CharField(max_length = 20, unique = True)
	descripcion = models.CharField(max_length = 100, unique = True)

	class Meta:
		app_label = 'registro'
		db_table = 'registro_tipo_conexion'
		ordering = ['nombre']

	def __unicode__(self):
		return self.nombre
