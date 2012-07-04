from django.db import models
from apps.registro.models.TipoConexion import TipoConexion
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.seguridad.audit import audit

#@audit
class ExtensionAulicaConexionInternet(models.Model):
    extension_aulica = models.ForeignKey('ExtensionAulica')
    tiene_conexion = models.BooleanField()
    tipo_conexion = models.ForeignKey('TipoConexion', null=True, blank=True)
    proveedor = models.CharField(max_length=30, null=True, blank=True)
    costo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)

    class Meta:
        app_label = 'registro'
        db_table = 'registro_extension_aulica_conexion_internet'
        ordering = ['proveedor']

    def __unicode__(self):
        return self.descripcion
