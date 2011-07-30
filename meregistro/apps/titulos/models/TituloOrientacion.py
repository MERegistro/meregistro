# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.Titulo import Titulo
import datetime

class TituloOrientacion(models.Model):
    titulo = models.ForeignKey(Titulo, related_name = 'orientaciones')
    nombre = models.CharField(max_length = 50)
    observaciones = models.CharField(max_length = 255, null = True, blank = True)
    fecha_alta = models.DateField(null = True, blank = True)

    class Meta:
        app_label = 'titulos'
        ordering = ['nombre']
        db_table = 'titulos_titulo_orientaciones'

    def __unicode__(self):
        return self.nombre

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(TituloOrientacion, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()
        self.estado_actual = self.getEstadoActual()

    def clean(self):
        "Es nuevo?"
        if self.id is None:
            self.fecha_alta = datetime.date.today()

    "Sobreescribo para eliminar lo estados"
    def delete(self, *args, **kwargs):
        for est in self.estados:
            est.delete()
        super(TituloOrientacion, self).delete(*args, **kwargs)

    def asociado_titulo_jurisdiccional(self):
        pass

    def registrar_estado(self, estado):
        from apps.titulos.models.TituloOrientacionEstado import TituloOrientacionEstado
        registro = TituloOrientacionEstado(estado = estado)
        registro.fecha = datetime.date.today()
        registro.titulo_orientacion_id = self.id
        registro.save()

    def getEstados(self):
        from apps.titulos.models.TituloOrientacionEstado import TituloOrientacionEstado
        try:
            estados = TituloOrientacionEstado.objects.filter(titulo_orientacion = self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados

    def getEstadoActual(self):
        try:
            return list(self.estados)[-1].estado
        except IndexError:
            return None
