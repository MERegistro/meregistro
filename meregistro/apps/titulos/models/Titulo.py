# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.TipoTitulo import TipoTitulo
from apps.titulos.models.TituloTipoNormativa import TituloTipoNormativa
from apps.titulos.models.Carrera import Carrera
from apps.titulos.models.Area import Area
from apps.registro.models.Nivel import Nivel
from apps.registro.models.Jurisdiccion import Jurisdiccion
import datetime

"""
Título nomenclado nacional
"""
class Titulo(models.Model):
    nombre = models.CharField(max_length = 200)
    tipo_titulo = models.ForeignKey(TipoTitulo)
    tipo_normativa = models.ForeignKey(TituloTipoNormativa)
    normativa = models.CharField(max_length = 50)
    carrera = models.ForeignKey(Carrera)
    tiene_orientaciones = models.BooleanField()
    observaciones = models.CharField(max_length = 255, null = True, blank = True)
    niveles = models.ManyToManyField(Nivel, db_table = 'titulos_titulos_niveles')
    areas = models.ManyToManyField(Area, db_table = 'titulos_titulos_areas')
    jurisdicciones = models.ManyToManyField(Jurisdiccion, db_table = 'titulos_titulos_jurisdicciones') # Provincias

    class Meta:
        app_label = 'titulos'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(Titulo, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()
        self.estado_actual = self.getEstadoActual()

    "Sobreescribo para eliminar lo estados"
    def delete(self, *args, **kwargs):
        for est in self.estados:
            est.delete()
        super(Titulo, self).delete(*args, **kwargs)

    def registrar_estado(self, estado):
        from apps.titulos.models.TituloEstado import TituloEstado
        registro = TituloEstado(estado = estado)
        registro.fecha = datetime.date.today()
        registro.titulo_id = self.id
        registro.save()

    def getEstados(self):
        from apps.titulos.models.TituloEstado import TituloEstado
        try:
            estados = TituloEstado.objects.filter(titulo = self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados

    def getEstadoActual(self):
        try:
            return list(self.estados)[-1].estado
        except IndexError:
            return None
