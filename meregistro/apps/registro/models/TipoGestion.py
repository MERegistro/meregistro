from django.db import models


class TipoGestion(models.Model):
    
    ESTATAL = u'Estatal'
    PRIVADA = u'Privada'
    
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = 'registro'
        db_table = 'registro_tipo_gestion'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre
