from django.db import models


class TipoSubsidio(models.Model):
    
    SIN_SUBSIDIO = '0%'
    
    descripcion = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = 'registro'
        db_table = 'registro_tipo_subsidio'
        ordering = ['descripcion']

    def __unicode__(self):
        return self.descripcion

    def delete(self):
        if (self.anexo_set.count() > 0
          or self.establecimiento_set.count() > 0
          or self.extensionaulica_set.count() > 0):
            raise Exception('Entidad en uso')
        models.Model.delete(self)
