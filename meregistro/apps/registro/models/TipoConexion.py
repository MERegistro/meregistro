from django.db import models


class TipoConexion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=100, unique=True)

    class Meta:
        app_label = 'registro'
        db_table = 'registro_tipo_conexion'
        ordering = ['descripcion']

    def __unicode__(self):
        return self.descripcion

    def delete(self):
        if (self.anexoconexioninternet_set.count() > 0
          or self.establecimientoconexioninternet_set.count() > 0
          or self.extensionaulicaconexioninternet_set.count() > 0):
            raise Exception('Entidad en uso')
        models.Model.delete(self)
