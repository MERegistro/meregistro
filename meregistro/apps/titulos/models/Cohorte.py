# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.Anexo import Anexo
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.titulos.models.CarreraJurisdiccional import CarreraJurisdiccional
import datetime

"Cada año de CarreraJurisdiccionalCohorte"
class Cohorte(models.Model):
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
        return CohorteEstablecimiento.objects.filter(cohorte = self, estado__nombre = EstadoCohorteEstablecimiento.ACEPTADA).exists()

    "Override del método para poder inertar un mensaje de error personalizado"
    "@see http://stackoverflow.com/questions/3993560/django-how-to-override-unique-together-error-message"
    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('carrera_jurisdiccional', 'anio'):
            return 'El título elegido ya tiene una cohorte asignada ese año.'
        else:
            return super(Cohorte, self).unique_error_message(model_class, unique_check)

    """
    Asocia/elimina los establecimientos desde el formulario masivo
    XXX: los valores "posts" vienen como strings
    """
    def save_establecimientos(self, current_establecimientos_ids, current_oferta_ids, current_emite_ids, post_ids, post_oferta_ids, post_emite_ids, estado):
        from apps.titulos.models.CohorteEstablecimiento import CohorteEstablecimiento
        "Borrar los que se des-chequean"
        for est_id in current_establecimientos_ids:
            if str(est_id) not in post_ids: # Si no está en los nuevos ids, borrarlo
                CohorteEstablecimiento.objects.get(cohorte = self, establecimiento = est_id).delete()

        "Agregar los nuevos"
        emite = None
        oferta = None
        for est_id in post_ids:
            "Emite u oferta??"
            if est_id in post_emite_ids:
                emite = True
            if est_id in post_oferta_ids:
                oferta = True
            "Si no está entre los actuales"
            if int(est_id) not in current_establecimientos_ids:
                # Lo creo y registro el estado
                registro = CohorteEstablecimiento.objects.create(cohorte = self, establecimiento_id = est_id, emite = emite, oferta = oferta, estado = estado)
                registro.registrar_estado()
            else:
                registro = CohorteEstablecimiento.objects.get(cohorte = self, establecimiento = est_id)
                registro.emite = emite
                registro.oferta = oferta
                registro.save()
                if str(registro.estado) != str(estado):
                    registro.registrar_estado()

    """
    Asocia/elimina los anexos desde el formulario masivo
    XXX: los valores "posts" vienen como strings
    """
    def save_anexos(self, current_anexos_ids, current_oferta_ids, current_emite_ids, post_ids, post_oferta_ids, post_emite_ids, estado):
        from apps.titulos.models.CohorteAnexo import CohorteAnexo
        "Borrar los que se des-chequean"
        for anexo_id in current_anexos_ids:
            if str(anexo_id) not in post_ids: # Si no está en los nuevos ids, borrarlo
                CohorteAnexo.objects.get(cohorte = self, anexo = anexo_id).delete()

        "Agregar los nuevos"
        emite = None
        oferta = None
        for anexo_id in post_ids:
            "Emite u oferta??"
            if anexo_id in post_emite_ids:
                emite = True
            if anexo_id in post_oferta_ids:
                oferta = True
            "Si no está entre los actuales"
            if int(anexo_id) not in current_anexos_ids:
                # Lo creo y registro el estado
                registro = CohorteAnexo.objects.create(cohorte = self, anexo_id = anexo_id, emite = emite, oferta = oferta, estado = estado)
                registro.registrar_estado()
            else:
                registro = CohorteAnexo.objects.get(cohorte = self, anexo = anexo_id)
                registro.emite = emite
                registro.oferta = oferta
                registro.save()
                if registro.estado != estado:
                    registro.registrar_estado()

    """
    Asocia/elimina las extensiones áulicas desde el formulario masivo
    XXX: los valores "posts" vienen como strings
    """
    def save_extensiones_aulicas(self, current_extensiones_aulicas_ids, current_oferta_ids, post_ids, post_oferta_ids, estado):
        from apps.titulos.models.CohorteExtensionAulica import CohorteExtensionAulica
        "Borrar los que se des-chequean"
        for extension_aulica_id in current_extensiones_aulicas_ids:
            if str(extension_aulica_id) not in post_ids: # Si no está en los nuevos ids, borrarlo
                CohorteExtensionAulica.objects.get(cohorte = self, extension_aulica = extension_aulica_id).delete()

        "Agregar los nuevos"
        oferta = None
        for extension_aulica_id in post_ids:
            "Oferta??"
            if extension_aulica_id in post_oferta_ids:
                oferta = True
            "Si no está entre los actuales"
            if int(extension_aulica_id) not in current_extensiones_aulicas_ids:
                # Lo creo y registro el estado
                registro = CohorteExtensionAulica.objects.create(cohorte = self, extension_aulica_id = extension_aulica_id, oferta = oferta, estado = estado)
                registro.registrar_estado()
            else:
                registro = CohorteExtensionAulica.objects.get(cohorte = self, extension_aulica = extension_aulica_id)
                registro.oferta = oferta
                registro.save()
                if registro.estado != estado:
                    registro.registrar_estado()
