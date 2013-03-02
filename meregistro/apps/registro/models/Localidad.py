from django.db import models
from apps.registro.models.Departamento import Departamento


class Localidad(models.Model):
    departamento = models.ForeignKey(Departamento)
    nombre = models.CharField(max_length=50)

    class Meta:
        app_label = 'registro'
        ordering = ['nombre']
        unique_together = ('departamento', 'nombre')

    def __unicode__(self):
        return self.nombre

    def delete(self):
        if (self.anexo_localidad.count() > 0
          or self.domicilios_establecimientos.count() > 0):
            raise Exception('Entidad en uso')
        models.Model.delete(self)
