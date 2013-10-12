from django.db import models


class EstadoExtensionAulica(models.Model):

    PENDIENTE = u'Pendiente'
    REGISTRADA = u'Registrada'
    NO_VIGENTE = u'No vigente'

    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = 'registro'
        ordering = ['nombre']
        db_table = 'registro_estado_extension_aulica'

    def __unicode__(self):
        return self.nombre
