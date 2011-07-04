from django.db import models


class Estado(models.Model):

    PENDIENTE = u'Pendiente'
    BAJA = u'Baja'
    REGISTRADO = u'Registrado'
    NO_VIGENTE = u'No vigente'
    VIGENTE = u'Vigente'

    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = 'registro'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre