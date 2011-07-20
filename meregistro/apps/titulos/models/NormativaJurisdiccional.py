# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.TipoNormativaJurisdiccional import TipoNormativaJurisdiccional
from apps.titulos.models.NormativaMotivoOtorgamiento import NormativaMotivoOtorgamiento
from apps.titulos.models.EstadoNormativaJurisdiccional import EstadoNormativaJurisdiccional
import datetime

class NormativaJurisdiccional(models.Model):
    numero_anio = models.CharField(max_length = 50)
    tipo_normativa_jurisdiccional = models.ForeignKey(TipoNormativaJurisdiccional)
    otorgada_por = models.ForeignKey(NormativaMotivoOtorgamiento)
    observaciones = models.CharField(max_length = 255, null = True, blank = True)
    estado = models.ForeignKey(EstadoNormativaJurisdiccional, ) # Concuerda con el último estado en NormativaJurisdiccionalEstado

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_normativa_jurisdiccional'

    """
    def __unicode__(self):
        return self.nombre
    """

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(NormativaJurisdiccional, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()

    "Sobreescribo para eliminar lo estados"
    def delete(self, *args, **kwargs):
        for est in self.estados:
            est.delete()
        super(NormativaJurisdiccional, self).delete(*args, **kwargs)

    def registrar_estado1(self, estado):
        from apps.titulos.models.NormativaJurisdiccionalEstado import NormativaJurisdiccionalEstado
        registro = NormativaJurisdiccionalEstado(estado = estado)
        registro.fecha = datetime.date.today()
        registro.normativa_jurisdiccional_id = self.id
        registro.save()

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

    # TODO:
    def __asociado_a_titulo_jurisdiccional(self):
        return

    # TODO:
    def isDeletable(self):
        return
