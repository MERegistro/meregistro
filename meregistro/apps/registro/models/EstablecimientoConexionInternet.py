from django.db import models
from apps.registro.models.TipoConexion import TipoConexion
from apps.registro.models.Establecimiento import Establecimiento
from apps.seguridad.audit import audit

@audit
class EstablecimientoConexionInternet(models.Model):
    establecimiento = models.ForeignKey('Establecimiento')
    tipo_conexion = models.ForeignKey('TipoConexion')
    proveedor = models.CharField(max_length=30)
    tiene_conexion = models.BooleanField()
    costo = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad = models.IntegerField()

    class Meta:
        app_label = 'registro'
        db_table = 'registro_establecimiento_conexion_internet'
        ordering = ['proveedor']

    def __unicode__(self):
        return self.descripcion
