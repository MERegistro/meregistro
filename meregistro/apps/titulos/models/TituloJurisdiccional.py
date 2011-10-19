# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.Titulo import Titulo
from apps.titulos.models.TipoTitulo import TipoTitulo
from apps.titulos.models.TituloOrientacion import TituloOrientacion
from apps.titulos.models.EstadoTituloJurisdiccional import EstadoTituloJurisdiccional
from apps.titulos.models.NormativaJurisdiccional import NormativaJurisdiccional
from apps.registro.models.Jurisdiccion import Jurisdiccion
import datetime

"""
Título jurisdiccional
"""

class TituloJurisdiccional(models.Model):
    #tipo_titulo = models.ForeignKey(TipoTitulo) -> Hereda del título
    titulo = models.ForeignKey(Titulo)
    orientaciones = models.ManyToManyField(TituloOrientacion, db_table = 'titulos_titulos_jurisd_orientaciones')
    normativas = models.ManyToManyField(NormativaJurisdiccional, db_table = 'titulos_titulos_jurisd_normativas')
    jurisdiccion = models.ForeignKey(Jurisdiccion)
    horas_reloj = models.PositiveIntegerField(null = True, blank = True)
    estado = models.ForeignKey(EstadoTituloJurisdiccional) # Concuerda con el último estado en TituloEstado
    revisado_jurisdiccion = models.NullBooleanField(default=False, null=True)
    # TituloJurisdiccionalCohorte -> datos_cohorte
    # TituloJurisdiccionalModalidadDistacia
    # TituloJurisdiccionalModalidadPresencial

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_titulo_jurisdiccional'
        ordering = ['id']

    def __unicode__(self):
        return self.titulo.nombre

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(TituloJurisdiccional, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()

    "Sobreescribo para eliminar lo objetos relacionados"
    def delete(self, *args, **kwargs):
        for est in self.estados:
            est.delete()
        try:
            self.modalidad_presencial.delete()
            self.modalidad_distancia.delete()
        except:
            pass
        super(TituloJurisdiccional, self).delete(*args, **kwargs)

    "Se eliminan las orientaciones, por ejemplo al cambiar el título"
    def eliminar_orientaciones(self):
        #for orientacion in self.orientaciones.all():
        #    orientacion.delete()
        pass

    def registrar_estado(self):
        from apps.titulos.models.TituloJurisdiccionalEstado import TituloJurisdiccionalEstado
        registro = TituloJurisdiccionalEstado(estado = self.estado)
        registro.fecha = datetime.date.today()
        registro.titulo_id = self.id
        registro.save()

    def getEstados(self):
        from apps.titulos.models.TituloJurisdiccionalEstado import TituloJurisdiccionalEstado
        try:
            estados = TituloJurisdiccionalEstado.objects.filter(titulo = self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados

    def getEstadoActual(self):
        try:
            return list(self.estados)[-1].estado
        except IndexError:
            return None

    def controlado(self):
        return self.estado.nombre == EstadoTituloJurisdiccional.CONTROLADO
