# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Jurisdiccion import Jurisdiccion
from apps.titulos.models.TipoNormativaJurisdiccional import TipoNormativaJurisdiccional
from apps.titulos.models.NormativaMotivoOtorgamiento import NormativaMotivoOtorgamiento
from apps.titulos.models.EstadoNormativaJurisdiccional import EstadoNormativaJurisdiccional
import datetime

class NormativaJurisdiccional(models.Model):
    numero_anio = models.CharField(max_length = 50)
    tipo_normativa_jurisdiccional = models.ForeignKey(TipoNormativaJurisdiccional)
    jurisdiccion = models.ForeignKey(Jurisdiccion)
    otorgada_por = models.ForeignKey(NormativaMotivoOtorgamiento)
    observaciones = models.CharField(max_length = 255, null = True, blank = True)
    estado = models.ForeignKey(EstadoNormativaJurisdiccional) # Concuerda con el último estado en NormativaJurisdiccionalEstado
    revisado_jurisdiccion = models.NullBooleanField(default=False, null=True)

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_normativa_jurisdiccional'

    def __unicode__(self):
        return self.numero_anio + " - " + self.otorgada_por.nombre 


    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(NormativaJurisdiccional, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()

    "Sobreescribo para eliminar lo estados"
    def delete(self, *args, **kwargs):
        for est in self.estados:
            est.delete()
        super(NormativaJurisdiccional, self).delete(*args, **kwargs)

    def registrar_estado(self):
        from apps.titulos.models.NormativaJurisdiccionalEstado import NormativaJurisdiccionalEstado
        registro = NormativaJurisdiccionalEstado(estado = self.estado)
        registro.fecha = datetime.date.today()
        registro.normativa_jurisdiccional_id = self.id
        registro.save()

    def getEstados(self):
        from apps.titulos.models.NormativaJurisdiccionalEstado import NormativaJurisdiccionalEstado
        try:
            estados = NormativaJurisdiccionalEstado.objects.filter(normativa_jurisdiccional = self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados

    "Algún título jurisdiccional está asociado a la normativa?"
    def asociado_carrera_jurisdiccional(self):
        from apps.titulos.models.CarreraJurisdiccional import CarreraJurisdiccional
        return CarreraJurisdiccional.objects.filter(normativas__id = self.id).exists()

    def asociado_solicitud_validez(self):
        from apps.validez_nacional.models.Solicitud import Solicitud
        return Solicitud.objects.filter(normativas_jurisdiccionales__id = self.id).exists()


    def puede_eliminarse(self):
        if self.asociado_carrera_jurisdiccional():
            return False
        if self.asociado_solicitud_validez():
            return False
        return True
        
