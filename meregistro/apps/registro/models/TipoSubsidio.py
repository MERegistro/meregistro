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
