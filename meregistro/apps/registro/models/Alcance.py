from django.db import models


class Alcance(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        app_label = 'registro'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre
