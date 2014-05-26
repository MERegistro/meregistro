# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models.EstadoPostitulo import EstadoPostitulo
from apps.postitulos.models.TipoPostitulo import TipoPostitulo
from apps.postitulos.models.PostituloTipoNormativa import PostituloTipoNormativa
from apps.postitulos.models.CarreraPostitulo import CarreraPostitulo
from apps.postitulos.models.AreaPostitulo import AreaPostitulo
from apps.registro.models.Nivel import Nivel
from apps.registro.models.Jurisdiccion import Jurisdiccion
import datetime

"""
Título nomenclado nacional
"""
class Postitulo(models.Model):
    nombre = models.CharField(max_length=255)
    tipo_normativa = models.ForeignKey(PostituloTipoNormativa)
    normativa = models.CharField(max_length=50)
    carrera_postitulo = models.ForeignKey(CarreraPostitulo)
    observaciones = models.CharField(max_length=255, null=True, blank=True)
    niveles = models.ManyToManyField(Nivel, db_table='postitulos_postitulos_niveles')
    areas = models.ManyToManyField(AreaPostitulo, db_table='postitulos_postitulos_areas')
    jurisdicciones = models.ManyToManyField(Jurisdiccion, db_table='postitulos_postitulos_jurisdicciones') # Provincias
    estado = models.ForeignKey(EstadoPostitulo) # Concuerda con el último estado en TituloEstado

    class Meta:
        app_label = 'postitulos'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(Postitulo, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()

    def registrar_estado(self):
        from apps.postitulos.models.PostituloEstado import PostituloEstado
        registro = PostituloEstado(estado = self.estado)
        registro.fecha = datetime.date.today()
        registro.postitulo_id = self.id
        registro.save()

    def getEstados(self):
        from apps.postitulos.models.PostituloEstado import PostituloEstado
        try:
            estados = PostituloEstado.objects.filter(postitulo = self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados

    "Algún título jurisdiccional está asociado al título?"
    def asociado_carrera_postitulo_jurisdiccional(self):
        from apps.postitulos.models.CarreraPostituloJurisdiccional import CarreraPostituloJurisdiccional
        return CarreraPostituloJurisdiccional.objects.filter(postitulo = self).exists()
