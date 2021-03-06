from django.db import models


class OrigenNorma(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        app_label = 'registro'
        db_table = 'registro_origen_norma'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre

    def delete(self):
        if (self.extensionaulica_set.count() > 0):
            raise Exception('Entidad en uso')
        models.Model.delete(self)
