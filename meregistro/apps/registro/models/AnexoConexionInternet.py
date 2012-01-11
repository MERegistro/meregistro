from django.db import models
from apps.registro.models.TipoConexion import TipoConexion
from apps.registro.models.Anexo import Anexo
from apps.seguridad.audit import audit

@audit
class AnexoConexionInternet(models.Model):
    anexo = models.ForeignKey('Anexo')
    tipo_conexion = models.ForeignKey('TipoConexion')
    proveedor = models.CharField(max_length=30)
    tiene_conexion = models.BooleanField()
    costo = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad = models.IntegerField()

    class Meta:
        app_label = 'registro'
        db_table = 'registro_anexo_conexion_internet'
        ordering = ['proveedor']

    def __unicode__(self):
        return self.descripcion
