# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.Anexo import Anexo
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.postitulos.models.CarreraPostituloJurisdiccional import CarreraPostituloJurisdiccional
import datetime

"Cada año de CarreraJurisdiccionalCohorte, o sea cada Cohorte Generada"
class CohortePostitulo(models.Model):
    
    PRIMER_ANIO = 1980
    ULTIMO_ANIO = 2050
    
    carrera_postitulo_jurisdiccional = models.ForeignKey(CarreraPostituloJurisdiccional, related_name='cohortes_postitulo')
    anio = models.PositiveIntegerField()
    observaciones = models.CharField(max_length = 255, null = True, blank = True)
    establecimientos = models.ManyToManyField(Establecimiento, through="CohortePostituloEstablecimiento")
    anexos = models.ManyToManyField(Anexo, through="CohortePostituloAnexo")
    extensiones_aulicas = models.ManyToManyField(ExtensionAulica, through="CohortePostituloExtensionAulica")
    revisado_jurisdiccion = models.NullBooleanField(default=False, null=True)

    class Meta:
        app_label = 'postitulos'
        ordering = ['anio']
        db_table = 'postitulos_cohorte_postitulo'
        unique_together = ('carrera_postitulo_jurisdiccional', 'anio')

    def __unicode__(self):
        return str(self.anio)

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(CohortePostitulo, self).__init__(*args, **kwargs)
        self.aceptada_por_establecimiento = self.aceptada_por_establecimiento()

    "Algún establecimiento está asociado a la cohorte?"
    def asignada_establecimiento(self):
        return self.establecimientos.exists()

    "Algún establecimiento aceptó la cohorte?"
    def aceptada_por_establecimiento(self):
        from apps.titulos.models.CohorteEstablecimiento import CohorteEstablecimiento
        from apps.titulos.models.EstadoCohorteEstablecimiento import EstadoCohorteEstablecimiento
        return CohortePostituloEstablecimiento.objects.filter(cohorte = self, estado__nombre = EstadoCohortePostituloEstablecimiento.REGISTRADA).exists()

    "Override del método para poder inertar un mensaje de error personalizado"
    "@see http://stackoverflow.com/questions/3993560/django-how-to-override-unique-together-error-message"
    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('carrera_postitulo_jurisdiccional', 'anio'):
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
                CohortePostituloEstablecimiento.objects.get(cohorte=self, establecimiento=est_id).delete()

        "Agregar los nuevos"
        for est_id in establecimientos_seleccionados_ids:
            "Si no está entre los actuales"
            if int(est_id) not in current_establecimientos_ids:
                # Lo creo y registro el estado
                registro = CohortePostituloEstablecimiento.objects.create(cohorte=self, establecimiento_id=est_id, estado=estado)
                registro.registrar_estado()
            else:
                registro = CohortePostituloEstablecimiento.objects.get(cohorte=self, establecimiento=est_id)
                old_estado = str(registro.estado)
                if old_estado == EstadoCohortePostituloEstablecimiento.RECHAZADA: # Si estaba rechazada, la pongo asignada de nuevo
                    registro.estado = estado

                registro.save()
                if str(old_estado) != str(estado):
                    registro.registrar_estado()

    """
    Asocia/elimina los anexos desde el formulario masivo
    XXX: los valores "posts" vienen como strings
    """
    def save_anexos(self, anexos_procesados_ids, current_anexos_ids, anexos_seleccionados_ids, estado):
        
        from apps.postitulos.models.CohortePostituloAnexo import CohortePostituloAnexo
        from apps.postitulos.models.EstadoCohortePostituloAnexo import EstadoCohortePostituloAnexo
        
        "Borrar los que se des-chequean"
        for anexo_id in anexos_procesados_ids:
            if (str(anexo_id) not in anexos_seleccionados_ids) and (anexo_id in current_anexos_ids): # Si no está en los ids de la página, borrarlo
                CohortePostituloAnexo.objects.get(cohorte=self, anexo=anexo_id).delete()

        "Agregar los nuevos"
        for anexo_id in anexos_seleccionados_ids:
            "Si no está entre los actuales"
            if int(anexo_id) not in current_anexos_ids:
                # Lo creo y registro el estado
                registro = CohortePostituloAnexo.objects.create(cohorte=self, anexo_id=anexo_id, estado=estado)
                registro.registrar_estado()
            else:
                registro = CohortePostituloAnexo.objects.get(cohorte=self, anexo=anexo_id)

                old_estado = str(registro.estado)
                if old_estado == EstadoCohortePostituloAnexo.RECHAZADA: # Si estaba rechazada, la pongo asignada de nuevo
                    registro.estado = estado

                registro.save()
                if str(old_estado) != str(estado):
                    registro.registrar_estado()

    """
    Asocia/elimina las extensiones áulicas desde el formulario masivo
    XXX: los valores "posts" vienen como strings
    """
    def save_extensiones_aulicas(self, extensiones_aulicas_procesadas_ids, current_extensiones_aulicas_ids, extensiones_aulicas_seleccionadas_ids, estado):
        
        from apps.titulos.models.CohortePostituloExtensionAulica import CohortePostituloExtensionAulica
        from apps.titulos.models.EstadoCohortePostituloExtensionAulica import EstadoCohortePostituloExtensionAulica
        
        "Borrar los que se des-chequean"
        for extension_aulica_id in extensiones_aulicas_procesadas_ids:
            if (str(extension_aulica_id) not in extensiones_aulicas_seleccionadas_ids) and (extension_aulica_id in current_extensiones_aulicas_ids): # Si no está en los ids de la página, borrarlo
                CohortePostituloExtensionAulica.objects.get(cohorte=self, extension_aulica=extension_aulica_id).delete()

        "Agregar los nuevos"
        for extension_aulica_id in extensiones_aulicas_seleccionadas_ids:
            "Si no está entre los actuales"
            if int(extension_aulica_id) not in current_extensiones_aulicas_ids:
                # Lo creo y registro el estado
                registro = CohortePostituloExtensionAulica.objects.create(cohorte=self, extension_aulica_id=extension_aulica_id, estado=estado)
                registro.registrar_estado()
            else:
                registro = CohortePostituloExtensionAulica.objects.get(cohorte=self, extension_aulica=extension_aulica_id)

                old_estado = str(registro.estado)
                if old_estado == EstadoPostituloCohorteExtensionAulica.RECHAZADA: # Si estaba rechazada, la pongo asignada de nuevo
                    registro.estado = estado

                registro.save()
                if str(old_estado) != str(estado):
                    registro.registrar_estado()


    def rechazada_por_establecimiento(self, establecimiento):
        from apps.postitulos.models.CohortePostituloEstablecimiento import CohortePostituloEstablecimiento
        try:
            cohorte_establecimiento = CohortePostituloEstablecimiento.objects.get(cohorte=self, establecimiento__id=establecimiento.id)
        except CohortePostituloEstablecimiento.DoesNotExist:
            return False
        return cohorte_establecimiento.rechazada()


    def rechazada_por_anexo(self, anexo):
        from apps.postitulos.models.CohortePostituloAnexo import CohortePostituloAnexo
        try:
            cohorte_anexo = CohortePostituloAnexo.objects.get(cohorte=self, anexo__id=anexo.id)
        except CohortePostituloAnexo.DoesNotExist:
            return False
        return cohorte_anexo.rechazada()


    def rechazada_por_extension_aulica(self, extension_aulica):
        from apps.postitulos.models.CohortePostituloExtensionAulica import CohortePostituloExtensionAulica
        try:
            cohorte_ea = CohortePostituloExtensionAulica.objects.get(cohorte=self, extension_aulica__id=extension_aulica.id)
        except CohortePostituloExtensionAulica.DoesNotExist:
            return False
        return cohorte_ea.rechazada()
