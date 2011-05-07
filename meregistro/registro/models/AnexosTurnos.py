# -*- coding: utf-8 -*-
from django.db import models
from meregistro.registro.models.Turno import Turno
from django.core.exceptions import ValidationError

class AnexosTurnos(models.Model):
	anexo = models.ForeignKey('registro.Anexo')
	turno = models.ForeignKey(Turno)

	class Meta:
		app_label = 'registro'
		db_table = 'registro_anexos_turnos'
