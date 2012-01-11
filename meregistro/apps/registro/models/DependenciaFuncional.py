from django.db import models
from django.core.exceptions import ValidationError
from apps.registro.models.Jurisdiccion import Jurisdiccion
from apps.registro.models.TipoGestion import TipoGestion
from apps.registro.models.TipoEducacion import TipoEducacion
from apps.registro.models.TipoDependenciaFuncional import TipoDependenciaFuncional
from apps.seguridad.models import Ambito
from apps.seguridad.audit import audit

@audit
class DependenciaFuncional(models.Model):
    nombre = models.CharField(max_length=255)
    jurisdiccion = models.ForeignKey(Jurisdiccion)
    tipo_gestion = models.ForeignKey(TipoGestion)
    tipo_dependencia_funcional = models.ForeignKey(TipoDependenciaFuncional)
    ambito = models.ForeignKey(Ambito, editable=False, null=True)

    class Meta:
        app_label = 'registro'
        db_table = 'registro_dependencia_funcional'
        ordering = ['nombre']
        unique_together = ('jurisdiccion', 'tipo_gestion', 'tipo_dependencia_funcional')

    def __unicode__(self):
        return self.nombre

    def clean(self):
        " Chequea que no se repita la misma dependencia funcional "
        jurisdiccion = self.jurisdiccion
        tipo_dependencia_funcional = self.tipo_dependencia_funcional
        tipo_gestion = self.tipo_gestion
        if jurisdiccion and tipo_dependencia_funcional and tipo_gestion:
            try:
                df = DependenciaFuncional.objects.get(jurisdiccion=jurisdiccion, tipo_dependencia_funcional=tipo_dependencia_funcional, tipo_gestion=tipo_gestion)
                if df and df != self:
                    raise ValidationError('Ya existe una dependencia funcional similar.')
            except DependenciaFuncional.DoesNotExist:
                pass

    def save(self):
        self.updateAmbito()
        models.Model.save(self)

    def updateAmbito(self):
        if self.pk is None or self.ambito is None:
            self.ambito = self.jurisdiccion.ambito.createChild(self.nombre)
        else:
            self.ambito.descripcion = self.nombre
            self.ambito.save()

    def hasEstablecimientos(self):
        from apps.registro.models.Establecimiento import Establecimiento
        establecimientos = Establecimiento.objects.filter(dependencia_funcional=self)
        return establecimientos.count() > 0
