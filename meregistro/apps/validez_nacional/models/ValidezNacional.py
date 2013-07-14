# -*- coding: utf-8 -*-
from django.db import models
from apps.validez_nacional.models import Solicitud
from apps.registro.models import Establecimiento, Anexo
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
	carrera = models.CharField(max_length=255, null=True)
	titulo_nacional = models.CharField(max_length=255, null=True)
	primera_cohorte = models.CharField(max_length=255, null=True)
	ultima_cohorte = models.CharField(max_length=255, null=True)
	dictamen_cofev = models.CharField(max_length=255, null=True)
	normativas_nacionales = models.CharField(max_length=255, null=True)
	normativa_jurisdiccional = models.CharField(max_length=255, null=True)
	temporal = models.BooleanField(default=True, editable=False)

	class Meta:
		app_label = 'validez_nacional'
		db_table = 'validez_nacional_validez_nacional'

		
	def calcular_nro_infd_establecimiento(self):
		establecimiento = Establecimiento.objects.get(pk=self.unidad_educativa_id)
		cod_jur = establecimiento.dependencia_funcional.jurisdiccion.prefijo
		tipo_gestion = str(establecimiento.dependencia_funcional.tipo_gestion.id)
		unidad_educativa_id = str(establecimiento.id).zfill(5)
		anio = str(datetime.date.today().year)[2:]
		titulo = 'T'
		id_unico = str(self.id).zfill(6)
		nro_infd = cod_jur + tipo_gestion + unidad_educativa_id + anio + titulo + id_unico
		return nro_infd

		
	def get_establecimiento(self):
		try:
			e = Establecimiento.objects.get(pk=self.unidad_educativa_id)
		except Establecimiento.DoesNotExist: 
			e = None
		return e


	def calcular_nro_infd_anexo(self):
		anexo = Anexo.objects.get(pk=self.unidad_educativa_id)
		cod_jur = anexo.establecimiento.dependencia_funcional.jurisdiccion.prefijo
		tipo_gestion = str(anexo.establecimiento.dependencia_funcional.tipo_gestion.id)
		unidad_educativa_id = str(anexo.establecimiento.id).zfill(5)
		anio = str(datetime.date.today().year)[2:]
		titulo = 'T'
		id_unico = str(self.id).zfill(6)
		nro_infd = cod_jur + tipo_gestion + unidad_educativa_id + anio + titulo + id_unico
		return nro_infd


	def get_anexo(self):
		try:
			a = Anexo.objects.get(pk=self.unidad_educativa_id)
		except Anexo.DoesNotExist:
			a = None
		return a


	def get_unidad_educativa(self):
		if self.tipo_unidad_educativa == self.TIPO_UE_SEDE:
			ue = self.get_establecimiento()
		elif self.tipo_unidad_educativa == self.TIPO_UE_ANEXO:
			ue = self.get_anexo()
		
		return ue
			
	def get_jurisdiccion(self):
		ue = self.get_unidad_educativa()
		if ue:
			if self.tipo_unidad_educativa == self.TIPO_UE_SEDE:
				return ue.dependencia_funcional.jurisdiccion
			elif self.tipo_unidad_educativa == self.TIPO_UE_ANEXO:
				return ue.establecimiento.dependencia_funcional.jurisdiccion
		else:
			return None
