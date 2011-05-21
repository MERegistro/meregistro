from django.db import models
from registro.models.Establecimiento import Establecimiento
from registro.models.TipoConexion import TipoConexion

class ConexionInternet(models.Model):
    establecimiento = models.ForeignKey('Establecimiento')
    tipo_conexion = models.ForeignKey('TipoConexion')
    proveedor = models.CharField(max_length = 30)
    tiene_conexion = models.BooleanField()
    costo = models.DecimalField(max_digits = 12, decimal_places = 2)
    cantidad = models.IntegerField()

    class Meta:
        app_label = 'registro'
        db_table = 'registro_conexion_internet'
        ordering = ['proveedor']

    def __unicode__(self):
        return self.descripcion
