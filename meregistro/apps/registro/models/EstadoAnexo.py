from django.db import models


class EstadoAnexo(models.Model):

    PENDIENTE = u'Pendiente'
    BAJA = u'Baja'
    REGISTRADO = u'Registrado'
    NO_VIGENTE = u'No vigente'
    VIGENTE = u'Vigente'

    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = 'registro'
        ordering = ['nombre']
        db_table = 'registro_estado_anexo'

    def __unicode__(self):
        return self.nombre
