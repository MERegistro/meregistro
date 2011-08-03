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
    tipo_titulo = models.ForeignKey(TipoTitulo)
    titulo = models.ForeignKey(Titulo)
    orientaciones = models.ManyToManyField(TituloOrientacion, db_table = 'titulos_titulos_jurisd_orientaciones')
    normativas = models.ManyToManyField(NormativaJurisdiccional, db_table = 'titulos_titulos_jurisd_normativas')
    jurisdiccion = models.ForeignKey(Jurisdiccion)
    estado = models.ForeignKey(EstadoTituloJurisdiccional) # Concuerda con el último estado en TituloEstado
    # TituloJurisdiccionalCohorte
    # TituloJurisdiccionalModalidadDistacia
    # TituloJurisdiccionalModalidadPresencial

    class Meta:
        app_label = 'titulos'
        db_table = 'titulos_titulo_jurisdiccional'
        ordering = ['id']

    def __unicode__(self):
        return self.titulo

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

"""

* Datos básicos

Titulo (nombre)
Tipo Titulo (Mediante Selector) (Nuevo – Transición - Equivalencias)
Titulo (Selector) Solo deben aparecer como resultado los titulos nomenclados nacionales generados mediante el <CU030.00_Alta titulo nomenclado nacional> cuyo estado sea Vigente y según tipo de titulo elegido en el campo anterior *1, correspondientes a ámbito del perfil. Caso contrario, no muestra datos
---------------------------------
* Orientaciones (titulo nacional)

Solo muestra datos en el caso que el título seleccionado tenga asociadas Orientaciones en el <CU31.00_ Alta orientaciones al Título nomenclado nacional>. Caso contrario, no muestra datos.
Selecciona orientaciones mediante checbox. Incluir una opción para seleccionar todas. Puede seleccionar una, varias o todas.

--- Si se cambia el título, hay que borrar las orientaciones asignadas actuales ---


* Datos del titulo jurisdiccional

---------------------------------
Opciones pedagógicas:

El usuario puede seleccionar una o ambas opciones.

* Presencial (check)

Evento del sistema: Si selecciona esta opción el sistema solicita los siguientes datos:

 * Años de duración de la carrera: ( Numérico >0 >= 4, no requerido))
 * Cuatrimestres: ( Numérico =>0 <= 2)


* A Distancia (check)

Evento del sistema: Si selecciona esta opción el sistema solicita los siguientes datos:

 * Años de duración de la carrera: ( Numérico >0 >= 4, requerido)
 * Cuatrimestres: ( Numérico =>0 <= 2, no requerido)
 * Número de dictamen: (texto 50)

Horas reloj:  Si Años de duración de la carrera es 4 ( Numérico >0 >= 2600) o Años de duración de la carrera es 5 ( Numérico >0 >= 2860); requerido

-----------------------------------

6.4 Normativas

Muestra en grilla, las normativas generadas mediante el < CU32-00_Alta normativa jurisdiccional > correspondientes al ámbito del usuario.

Numero / Año | Tipo Normativa | Otorgada por | Seleccionar
 

Selecciona normativas mediante checbox. Incluir una opción para seleccionar todas. Puede seleccionar una, varias o todas.

------------------------------------

7.4 Cohortes autorizadas

Cohortes aprobadas: ( Numérico >0 < 5, requerido)
Año primera cohorte: (Selector año calendario, requerido)
Año ultima cohorte: (Selector año calendario, requerido)
Observaciones: Texto, no requerido
------------------------------------
7. Confirma los datos cargados mediante el botón Guardar.

8. El sistema asigna en forma automática el estado Controlado.
"""
