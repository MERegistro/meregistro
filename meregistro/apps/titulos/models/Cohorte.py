# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.titulos.models.TituloJurisdiccional import TituloJurisdiccional
import datetime

"Cada año de TituloJurisdiccionalCohorte"
class Cohorte(models.Model):
    titulo_jurisdiccional = models.ForeignKey(TituloJurisdiccional, related_name = 'cohortes')
    anio = models.PositiveIntegerField()
    observaciones = models.CharField(max_length = 255, null = True, blank = True)
    establecimientos = models.ManyToManyField(Establecimiento, through = "CohorteEstablecimiento")

    class Meta:
        app_label = 'titulos'
        ordering = ['anio']
        db_table = 'titulos_cohorte'
        unique_together = ('titulo_jurisdiccional', 'anio')

    def __unicode__(self):
        return str(self.anio)

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(Cohorte, self).__init__(*args, **kwargs)

    "Algún establecimiento está asociado a la cohorte?"
    def asignada_establecimiento(self):
        return self.establecimientos.exists()


    "Override del método para poder inertar un mensaje de error personalizado"
    "@see http://stackoverflow.com/questions/3993560/django-how-to-override-unique-together-error-message"
    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('titulo_jurisdiccional', 'anio'):
            return 'El título elegido ya tiene una cohorte asignada ese año.'
        else:
            return super(Cohorte, self).unique_error_message(model_class, unique_check)
