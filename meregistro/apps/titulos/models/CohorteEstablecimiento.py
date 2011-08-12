# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.titulos.models.Cohorte import Cohorte
from apps.titulos.models.EstadoCohorteEstablecimiento import EstadoCohorteEstablecimiento
import datetime

"Cada año de TituloJurisdiccionalCohorte"
class CohorteEstablecimiento(models.Model):
    establecimiento = models.ForeignKey(Establecimiento)
    cohorte = models.ForeignKey(Cohorte)
    estado = models.ForeignKey(EstadoCohorteEstablecimiento) # Concuerda con el último estado en CohorteEstablecimientoEstado

    class Meta:
        app_label = 'titulos'
        ordering = ['cohorte__anio']
        db_table = 'titulos_cohortes_establecimientos'

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(CohorteEstablecimiento, self).__init__(*args, **kwargs)

    "Algún establecimiento está asociado a la cohorte?"
    def asignada_establecimiento(self):
        return self.establecimientos.exists()

