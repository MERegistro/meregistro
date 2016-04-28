# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.titulos.models.Cohorte import Cohorte
from apps.titulos.models.EstadoCohorteExtensionAulica import EstadoCohorteExtensionAulica
import datetime

"Cada asignación de una cohorte a un anexo"
class CohorteExtensionAulica(models.Model):
    extension_aulica = models.ForeignKey(ExtensionAulica, related_name='cohortes')
    cohorte = models.ForeignKey(Cohorte)
    inscriptos = models.PositiveIntegerField(null=True)
    estado = models.ForeignKey(EstadoCohorteExtensionAulica) # Concuerda con el último estado en CohorteExtensionAulicaEstado


    class Meta:
        app_label = 'titulos'
        ordering = ['cohorte__anio']
        db_table = 'titulos_cohortes_extensiones_aulicas'
        unique_together = ('extension_aulica', 'cohorte')


    def __unicode__(self):
        return str(self.extension_aulica) + ' - ' + str(self.cohorte)


    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(CohorteExtensionAulica, self).__init__(*args, **kwargs)
        self.estados = self.get_estados()


    "La cohorte fue aceptada por la extensión áulica?"
    def registrada(self):
        return self.estado.nombre == EstadoCohorteExtensionAulica.REGISTRADA


    "La cohorte fue rechazada por la extensión áulica?"
    def rechazada(self):
        return self.estado.nombre == EstadoCohorteExtensionAulica.RECHAZADA


    "La cohorte (su seguimiento) fue finalizada por el establecimiento?"
    def finalizada(self):
        return self.estado.nombre == EstadoCohorteExtensionAulica.FINALIZADA

    def registrar_estado(self):
        from apps.titulos.models.CohorteExtensionAulicaEstado import CohorteExtensionAulicaEstado
        registro = CohorteExtensionAulicaEstado(estado=self.estado)
        registro.fecha = datetime.date.today()
        registro.cohorte_extension_aulica_id = self.id
        registro.save()


    def get_estados(self):
        from apps.titulos.models.CohorteExtensionAulicaEstado import CohorteExtensionAulicaEstado
        try:
            estados = CohorteExtensionAulicaEstado.objects.filter(cohorte_extension_aulica=self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados
        
        
    def tiene_seguimiento(self):
        return len(self.seguimiento.all()) > 0
    
    
    def is_editable(self):
        return self.registrada() and not self.tiene_seguimiento()
            
        
    def is_rechazable(self):
        return not self.rechazada() and self.inscriptos == None
    
        
    def get_ultimo_seguimiento_cargado(self):
        return self.seguimiento.all().order_by('-anio')[:1]
            
            
    def get_total_egresados(self):
        total = 0
        for s in self.seguimiento.all():
            total = total + s.egresados
        return total

        
    def get_establecimiento(self):
        return self.extension_aulica.establecimiento

        
    def get_unidad_educativa(self):
        return self.extension_aulica
