# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.titulos.models.Cohorte import Cohorte
from apps.titulos.models.EstadoCohorteEstablecimiento import EstadoCohorteEstablecimiento
import datetime
    
"Cada asignación de una cohorte a un establecimiento"
class CohorteEstablecimiento(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, related_name='cohortes')
    cohorte = models.ForeignKey(Cohorte)
    inscriptos = models.PositiveIntegerField(null=True)
    estado = models.ForeignKey(EstadoCohorteEstablecimiento) # Concuerda con el último estado en CohorteEstablecimientoEstado

    class Meta:
        app_label = 'titulos'
        ordering = ['cohorte__anio']
        db_table = 'titulos_cohortes_establecimientos'
        unique_together = ('establecimiento', 'cohorte')


    def __unicode__(self):
        return str(self.establecimiento) + ' - ' + str(self.cohorte)


    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(CohorteEstablecimiento, self).__init__(*args, **kwargs)
        self.estados = self.get_estados()


    "La cohorte fue aceptada por el establecimiento?"
    def registrada(self):
        return self.estado.nombre == EstadoCohorteEstablecimiento.REGISTRADA

    "La cohorte fue rechazada por el establecimiento?"
    def rechazada(self):
        return self.estado.nombre == EstadoCohorteEstablecimiento.RECHAZADA

    "La cohorte (su seguimiento) fue finalizada por el establecimiento?"
    def finalizada(self):
        return self.estado.nombre == EstadoCohorteEstablecimiento.FINALIZADA


    def registrar_estado(self):
        from apps.titulos.models.CohorteEstablecimientoEstado import CohorteEstablecimientoEstado
        registro = CohorteEstablecimientoEstado(estado=self.estado)
        registro.fecha = datetime.date.today()
        registro.cohorte_establecimiento_id = self.id
        registro.save()


    def get_estados(self):
        from apps.titulos.models.CohorteEstablecimientoEstado import CohorteEstablecimientoEstado
        try:
            estados = CohorteEstablecimientoEstado.objects.filter(cohorte_establecimiento=self).order_by('fecha', 'id')
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
        return self.establecimiento

        
    def get_unidad_educativa(self):
        return self.establecimiento
