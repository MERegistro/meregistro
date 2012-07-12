# -*- coding: utf-8 -*-
from django.db import models


class TipoCompartido(models.Model):

    TIPO_OTRO_INSTITUTO = 'Otro Instituto Superior de Formación Docente'
    TIPO_OTRO_TIPO_INSTITUCION = 'Otro Tipo de Institución'
    TIPO_OTRA_INSTITUCION = 'Otra Institución Educativa'
    
    descripcion = models.CharField(max_length = 50, unique = True)

    class Meta:
        app_label = 'registro'
        db_table = 'registro_tipo_compartido'
        ordering = ['descripcion']

    def __unicode__(self):
        return self.descripcion

    def delete(self):
        if (self.anexoinformacionedilicia_set.count() > 0
          or self.anexoturno_set.count() > 0
          or self.establecimientoinformacionedilicia_set.count() > 0
          or self.establecimientoturno_set.count() > 0
          or self.extensionaulicainformacionedilicia_set.count() > 0
          or self.extensionaulicaturno_set.count() > 0):
            raise Exception('Entidad en uso')
        models.Model.delete(self)
