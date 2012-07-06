# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Anexo import Anexo
from apps.seguridad.audit import audit


@audit
class AnexoMatricula(models.Model):
    anexo = models.ForeignKey(Anexo)
    anio = models.IntegerField()
    mixto = models.BooleanField()
    profesorados = models.PositiveIntegerField(null=True, blank=True)
    postitulos = models.PositiveIntegerField(null=True, blank=True)
    formacion_docente = models.PositiveIntegerField(null=True, blank=True)
    formacion_continua = models.PositiveIntegerField(null=True, blank=True)
    tecnicaturas = models.PositiveIntegerField(null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        app_label = 'registro'
        unique_together = ('anexo', 'anio')
        db_table = 'registro_anexo_matricula'

    def get_formacion_docente(self):
		# Formación Docente = Sólo Profesorados + Sólo Postítulos + Formación contínua 
        tmp = ((self.profesorados or 0) + (self.postitulos or 0)) + (self.formacion_continua or 0)
        if tmp <= 0:
            return None
        return tmp

    def get_formacion_continua(self):
		# Formación contínua = Total - Sólo Tecnicaturas - Sólo Profesorados - Sólo Postítulos
        tmp = ((self.total or 0) - (self.tecnicaturas or 0)) - (self.profesorados or 0) - (self.postitulos or 0) or None
        if tmp <= 0:
            return None
        return tmp

    def set_formacion_docente(self):
        self.formacion_docente = self.get_formacion_docente()

    def set_formacion_continua(self):
        self.formacion_continua = self.get_formacion_continua()
