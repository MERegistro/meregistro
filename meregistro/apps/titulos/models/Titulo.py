# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.EstadoTitulo import EstadoTitulo
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
    estado = models.ForeignKey(EstadoTitulo) # Concuerda con el último estado en TituloEstado

    class Meta:
        app_label = 'titulos'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(Titulo, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()

    "Sobreescribo para eliminar los objetos relacionados"
    def delete(self, *args, **kwargs):
        for orientacion in self.orientaciones.all():
            orientacion.delete()
        for est in self.estados.all():
            est.delete()
        super(Titulo, self).delete(*args, **kwargs)

    def registrar_estado(self):
        from apps.titulos.models.TituloEstado import TituloEstado
        registro = TituloEstado(estado = self.estado)
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

    "Algún título jurisdiccional está asociado al título?"
    def asociado_titulo_jurisdiccional(self):
        from apps.titulos.models.TituloJurisdiccional import TituloJurisdiccional
        return TituloJurisdiccional.objects.filter(titulo = self).exists()
