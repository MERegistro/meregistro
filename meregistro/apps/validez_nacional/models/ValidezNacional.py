# -*- coding: utf-8 -*-
from django.db import models
from apps.validez_nacional.models import Solicitud
import datetime

"""
Título nacional Validado por el INFOD
"""
class ValidezNacional(models.Model):
	
	TIPO_UE_SEDE = u'Sede'
	TIPO_UE_ANEXO = u'Anexo'

	solicitud = models.ForeignKey(Solicitud, null=False, related_name="validez_nacional")
	nro_infd = models.CharField(max_length=99, null=False)
	cue = models.CharField(max_length=9, null=False, db_index=True)
	tipo_unidad_educativa = models.CharField(max_length=10, null=False)
	unidad_educativa_id = models.PositiveIntegerField(null=False)

	class Meta:
		app_label = 'validez_nacional'
		db_table = 'validez_nacional_validez_nacional'

