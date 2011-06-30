from django.db import models
from meregistro.apps.titulos.models.TipoTitulo import TipoTitulo
from meregistro.apps.registro.models.TipoNormativa import TipoNormativa
from meregistro.apps.titulos.models.Carrera import Carrera
from meregistro.apps.titulos.models.Area import Area
from meregistro.apps.registro.models.Nivel import Nivel
from meregistro.apps.registro.models.Jurisdiccion import Jurisdiccion

class Titulo(models.Model):
    nombre = models.CharField(max_length = 200)
    tipo_titulo = models.ForeignKey(TipoTitulo)
    tipo_normativa = models.ForeignKey(TipoNormativa)
    normativa = models.CharField(max_length = 50, null = True, blank = True)
    carrera = models.ForeignKey(Carrera)
    tiene_orientaciones = models.BooleanField()
    observaciones = models.CharField(max_length = 255, null = True, blank = True)
    niveles = models.ManyToManyField(Nivel, null = True, db_table = 'titulos_titulos_niveles')
    areas = models.ManyToManyField(Area, null = True, db_table = 'titulos_titulos_areas')
    jurisdicciones = models.ManyToManyField(Jurisdiccion, null = True, db_table = 'titulos_titulos_jurisdicciones') # Provincias

    class Meta:
        app_label = 'titulos'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre
