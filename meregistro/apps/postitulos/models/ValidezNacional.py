# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models import Solicitud
from apps.registro.models import Establecimiento, Anexo
import datetime

"""
Título nacional Validado por el INFOD
"""
class ValidezNacional(models.Model):
	
	TIPO_UE_SEDE = u'Sede'
	TIPO_UE_ANEXO = u'Anexo'

	solicitud = models.ForeignKey(Solicitud, null=False, related_name="validez_nacional_postitulo")
	nro_infd = models.CharField(max_length=99, null=False)
	cue = models.CharField(max_length=9, null=False, db_index=True)
	tipo_unidad_educativa = models.CharField(max_length=10, null=False)
	unidad_educativa_id = models.PositiveIntegerField(null=False)
	carrera_postitulo = models.CharField(max_length=255, null=True)
	postitulo_nacional = models.CharField(max_length=255, null=True)
	primera_cohorte = models.CharField(max_length=255, null=True)
	ultima_cohorte = models.CharField(max_length=255, null=True)
	normativas_postitulo = models.CharField(max_length=255, null=True)
	normativa_postitulo_jurisdiccional = models.CharField(max_length=255, null=True)
	referencia = models.CharField(max_length=10, null=True, editable=False)

	class Meta:
		app_label = 'postitulos'
		db_table = 'postitulos_validez_nacional'

		
	def calcular_nro_infd_establecimiento(self):
		establecimiento = Establecimiento.objects.get(pk=self.unidad_educativa_id)
		cod_jur = establecimiento.dependencia_funcional.jurisdiccion.prefijo
		tipo_gestion = str(establecimiento.dependencia_funcional.tipo_gestion.id)
		unidad_educativa_id = str(establecimiento.id).zfill(5)
		anio = str(datetime.date.today().year)[2:]
		postitulo = 'P'
		id_unico = str(self.id).zfill(6)
		nro_infd = cod_jur + tipo_gestion + unidad_educativa_id + anio + postitulo + id_unico
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
		postitulo = 'P'
		id_unico = str(self.id).zfill(6)
		nro_infd = cod_jur + tipo_gestion + unidad_educativa_id + anio + postitulo + id_unico
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
			
	def get_domicilio_institucional(self):
		return self.get_unidad_educativa().get_domicilio_institucional()
		
		
	"Sobreescribo para eliminar los objetos relacionados"
	def delete(self, *args, **kwargs):
		for est_sol in self.solicitud.establecimientos_postitulo.all():
			est_sol.delete()
		for anexo_sol in self.solicitud.anexos_postitulo.all():
			anexo_sol.delete()
		super(ValidezNacional, self).delete(*args, **kwargs)
