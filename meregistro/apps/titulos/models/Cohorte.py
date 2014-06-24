# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.Anexo import Anexo
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.titulos.models.CarreraJurisdiccional import CarreraJurisdiccional
import datetime

"Cada año de CarreraJurisdiccionalCohorte, o sea cada Cohorte Generada"
class Cohorte(models.Model):
    
    PRIMER_ANIO = 1980
    ULTIMO_ANIO = 2050
    
    carrera_jurisdiccional = models.ForeignKey(CarreraJurisdiccional, related_name='cohortes')
    anio = models.PositiveIntegerField()
    observaciones = models.CharField(max_length = 255, null = True, blank = True)
    establecimientos = models.ManyToManyField(Establecimiento, through="CohorteEstablecimiento")
    anexos = models.ManyToManyField(Anexo, through="CohorteAnexo")
    extensiones_aulicas = models.ManyToManyField(ExtensionAulica, through="CohorteExtensionAulica")
    revisado_jurisdiccion = models.NullBooleanField(default=False, null=True)

    class Meta:
        app_label = 'titulos'
        ordering = ['anio']
        db_table = 'titulos_cohorte'
        unique_together = ('carrera_jurisdiccional', 'anio')

    def __unicode__(self):
        return str(self.anio)

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(Cohorte, self).__init__(*args, **kwargs)
        self.aceptada_por_establecimiento = self.aceptada_por_establecimiento()

    "Algún establecimiento está asociado a la cohorte?"
    def asignada_establecimiento(self):
        return self.establecimientos.exists()

    "Algún establecimiento aceptó la cohorte?"
    def aceptada_por_establecimiento(self):
        from apps.titulos.models.CohorteEstablecimiento import CohorteEstablecimiento
        from apps.titulos.models.EstadoCohorteEstablecimiento import EstadoCohorteEstablecimiento
        return CohorteEstablecimiento.objects.filter(cohorte = self, estado__nombre = EstadoCohorteEstablecimiento.REGISTRADA).exists()

    "Override del método para poder inertar un mensaje de error personalizado"
    "@see http://stackoverflow.com/questions/3993560/django-how-to-override-unique-together-error-message"
    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('carrera_jurisdiccional', 'anio'):
            return 'La carrera ya tiene una cohorte asignada ese año.'
        else:
            return super(Cohorte, self).unique_error_message(model_class, unique_check)

    """
    Asocia/elimina los establecimientos desde el formulario masivo
    XXX: los valores "posts" vienen como strings
    """
    def save_establecimientos(self, establecimientos_procesados_ids, current_establecimientos_ids, establecimientos_seleccionados_ids, estado):
        from apps.titulos.models.CohorteEstablecimiento import CohorteEstablecimiento
        from apps.titulos.models.EstadoCohorteEstablecimiento import EstadoCohorteEstablecimiento
        
        "Borrar los que se des-chequean"
        for est_id in establecimientos_procesados_ids:
            if (str(est_id) not in establecimientos_seleccionados_ids) and (est_id in current_establecimientos_ids): # Si no está en los ids de la página, borrarlo
                CohorteEstablecimiento.objects.get(cohorte=self, establecimiento=est_id).delete()

        "Agregar los nuevos"
        for est_id in establecimientos_seleccionados_ids:
            "Si no está entre los actuales"
            if int(est_id) not in current_establecimientos_ids:
                # Lo creo y registro el estado
                registro = CohorteEstablecimiento.objects.create(cohorte=self, establecimiento_id=est_id, estado=estado)
                registro.registrar_estado()
            else:
                registro = CohorteEstablecimiento.objects.get(cohorte=self, establecimiento=est_id)
                old_estado = str(registro.estado)
                if old_estado == EstadoCohorteEstablecimiento.RECHAZADA: # Si estaba rechazada, la pongo asignada de nuevo
                    registro.estado = estado

                registro.save()
                if str(old_estado) != str(estado):
                    registro.registrar_estado()

    """
    Asocia/elimina los anexos desde el formulario masivo
    XXX: los valores "posts" vienen como strings
    """
    def save_anexos(self, anexos_procesados_ids, current_anexos_ids, anexos_seleccionados_ids, estado):
        
        from apps.titulos.models.CohorteAnexo import CohorteAnexo
        from apps.titulos.models.EstadoCohorteAnexo import EstadoCohorteAnexo
        
        "Borrar los que se des-chequean"
        for anexo_id in anexos_procesados_ids:
            if (str(anexo_id) not in anexos_seleccionados_ids) and (anexo_id in current_anexos_ids): # Si no está en los ids de la página, borrarlo
                CohorteAnexo.objects.get(cohorte=self, anexo=anexo_id).delete()

        "Agregar los nuevos"
        for anexo_id in anexos_seleccionados_ids:
            "Si no está entre los actuales"
            if int(anexo_id) not in current_anexos_ids:
                # Lo creo y registro el estado
                registro = CohorteAnexo.objects.create(cohorte=self, anexo_id=anexo_id, estado=estado)
                registro.registrar_estado()
            else:
                registro = CohorteAnexo.objects.get(cohorte=self, anexo=anexo_id)

                old_estado = str(registro.estado)
                if old_estado == EstadoCohorteAnexo.RECHAZADA: # Si estaba rechazada, la pongo asignada de nuevo
                    registro.estado = estado

                registro.save()
                if str(old_estado) != str(estado):
                    registro.registrar_estado()

    """
    Asocia/elimina las extensiones áulicas desde el formulario masivo
    XXX: los valores "posts" vienen como strings
    """
    def save_extensiones_aulicas(self, extensiones_aulicas_procesadas_ids, current_extensiones_aulicas_ids, extensiones_aulicas_seleccionadas_ids, estado):
        
        from apps.titulos.models.CohorteExtensionAulica import CohorteExtensionAulica
        from apps.titulos.models.EstadoCohorteExtensionAulica import EstadoCohorteExtensionAulica
        
        "Borrar los que se des-chequean"
        for extension_aulica_id in extensiones_aulicas_procesadas_ids:
            if (str(extension_aulica_id) not in extensiones_aulicas_seleccionadas_ids) and (extension_aulica_id in current_extensiones_aulicas_ids): # Si no está en los ids de la página, borrarlo
                CohorteExtensionAulica.objects.get(cohorte=self, extension_aulica=extension_aulica_id).delete()

        "Agregar los nuevos"
        for extension_aulica_id in extensiones_aulicas_seleccionadas_ids:
            "Si no está entre los actuales"
            if int(extension_aulica_id) not in current_extensiones_aulicas_ids:
                # Lo creo y registro el estado
                registro = CohorteExtensionAulica.objects.create(cohorte=self, extension_aulica_id=extension_aulica_id, estado=estado)
                registro.registrar_estado()
            else:
                registro = CohorteExtensionAulica.objects.get(cohorte=self, extension_aulica=extension_aulica_id)

                old_estado = str(registro.estado)
                if old_estado == EstadoCohorteExtensionAulica.RECHAZADA: # Si estaba rechazada, la pongo asignada de nuevo
                    registro.estado = estado

                registro.save()
                if str(old_estado) != str(estado):
                    registro.registrar_estado()


    def rechazada_por_establecimiento(self, establecimiento):
        from apps.titulos.models.CohorteEstablecimiento import CohorteEstablecimiento
        try:
            cohorte_establecimiento = CohorteEstablecimiento.objects.get(cohorte__id=self.id, establecimiento__id=establecimiento.id)
        except CohorteEstablecimiento.DoesNotExist:
            return False
        return cohorte_establecimiento.rechazada()


    def rechazada_por_anexo(self, anexo):
        from apps.titulos.models.CohorteAnexo import CohorteAnexo
        try:
            cohorte_anexo = CohorteAnexo.objects.get(cohorte=self, anexo__id=anexo.id)
        except CohorteAnexo.DoesNotExist:
            return False
        return cohorte_anexo.rechazada()


    def rechazada_por_extension_aulica(self, extension_aulica):
        from apps.titulos.models.CohorteExtensionAulica import CohorteExtensionAulica
        try:
            cohorte_ea = CohorteExtensionAulica.objects.get(cohorte=self, extension_aulica__id=extension_aulica.id)
        except CohorteExtensionAulica.DoesNotExist:
            return False
        return cohorte_ea.rechazada()
