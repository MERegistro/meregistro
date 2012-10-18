# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.Titulo import Titulo
from apps.titulos.models.EstadoTituloOrientacion import EstadoTituloOrientacion
import datetime

class TituloOrientacion(models.Model):
    titulo = models.ForeignKey(Titulo, related_name = 'orientaciones')
    nombre = models.CharField(max_length = 50)
    observaciones = models.CharField(max_length = 255, null = True, blank = True)
    fecha_alta = models.DateField(null = True, blank = True)
    estado = models.ForeignKey(EstadoTituloOrientacion) # Concuerda con el último estado en TituloOrientacionEstado

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

    def clean(self):
        "Es nuevo?"
        if self.id is None:
            self.fecha_alta = datetime.date.today()

    "Sobreescribo para eliminar lo estados"
    def delete(self, *args, **kwargs):
        for est in self.estados:
            est.delete()
        super(TituloOrientacion, self).delete(*args, **kwargs)

    def asociado_carrera_jurisdiccional(self):
        pass

    def registrar_estado(self):
        from apps.titulos.models.TituloOrientacionEstado import TituloOrientacionEstado
        registro = TituloOrientacionEstado(estado = self.estado)
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

    "Algún título jurisdiccional está asociado a la orientación?"
    def asociado_carrera_jurisdiccional(self):
        from apps.titulos.models.CarreraJurisdiccional import CarreraJurisdiccional
        return CarreraJurisdiccional.objects.filter(orientaciones__id = self.id).exists()
