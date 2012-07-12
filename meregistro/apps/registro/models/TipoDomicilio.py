from django.db import models


class TipoDomicilio(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = 'registro'
        db_table = 'registro_tipo_domicilio'
        ordering = ['descripcion']

    def __unicode__(self):
        return self.descripcion

    def delete(self):
        if (self.anexodomicilio_set.count() > 0
          or self.establecimientodomicilio_set.count() > 0
          or self.extensionaulicadomicilio_set.count() > 0):
            raise Exception('Entidad en uso')
        models.Model.delete(self)
