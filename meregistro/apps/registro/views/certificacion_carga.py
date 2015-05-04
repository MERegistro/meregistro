# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import TipoAmbito
from apps.registro.models import Jurisdiccion, Establecimiento, Anexo, ExtensionAulica
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
import datetime

ITEMS_PER_PAGE = 50
ANIOS_HABILITADOS = ['2015']

@login_required    
def __get_ue_actual(request, tipo):
    """
    Trae la unidad educativa del usuario
    """
    if tipo.nombre == TipoAmbito.TIPO_SEDE:
        return Establecimiento.objects.get(ambito__id=request.get_perfil().ambito.id)
    elif tipo.nombre == TipoAmbito.TIPO_ANEXO:
        return Anexo.objects.get(ambito__id=request.get_perfil().ambito.id)
    elif tipo.nombre == TipoAmbito.TIPO_EXTENSION_AULICA:
        return ExtensionAulica.objects.get(ambito__id=request.get_perfil().ambito.id)
    else:
        raise Exception('ERROR: El usuario no tiene asignado una unidad educativa.')

"""
Pantalla en la cual se listan las unidades educativas del usuario
"""
@login_required
#@credential_required('tit_cohorte_seguimiento_consulta')
def index(request, anio):
    if not anio in ANIOS_HABILITADOS:
        raise Exception('ERROR: El año no está disponible para certificar la carga.')
        
    tipo_perfil = request.get_perfil().ambito.tipo
    
    unidad_educativa = __get_ue_actual(request, tipo_perfil)
    
    if unidad_educativa.__class__ == Establecimiento:
        establecimiento = unidad_educativa
    elif unidad_educativa.__class__ == Anexo or unidad_educativa.__class__ == ExtensionAulica:
        establecimiento = unidad_educativa.establecimiento
    
    anexos = establecimiento.anexos
    extensiones_aulicas = establecimiento.extensiones_aulicas

    return my_render(request, 'registro/certificacion_carga/index.html', {
        'anio': anio,
        'establecimiento': establecimiento,
        'anexos': anexos.all(),
        'extensiones_aulicas': extensiones_aulicas.all(),
        'unidad_educativa_actual': unidad_educativa,
        'tipo_perfil': tipo_perfil.nombre
    })


@login_required
#@credential_required('tit_cohorte_aceptar_asignacion')
def certificar_establecimiento(request, anio, establecimiento_id):
    if not anio in ANIOS_HABILITADOS:
        raise Exception('ERROR: El año no está disponible para certificar la carga.')

    establecimiento = Establecimiento.objects.get(id=establecimiento_id, ambito__path=request.get_perfil().ambito.path)

    return my_render(request, 'registro/certificacion_carga/certificar_establecimiento.html', {
        'anio': anio,
        'establecimiento': establecimiento,
        'puede_certificar_carga': establecimiento.puede_certificar_carga(anio)
    })

@login_required
#@credential_required('tit_cohorte_aceptar_asignacion')
def rechazar(request, cohorte_ue_id, tipo_unidad_educativa):
    """
    Rechazar cohorte
    """
    if tipo_unidad_educativa == 'establecimiento':
        cohorte_unidad_educativa = CohorteEstablecimiento.objects.get(pk=cohorte_ue_id, establecimiento__ambito__path__istartswith=request.get_perfil().ambito.path)
        unidad_educativa = cohorte_unidad_educativa.establecimiento
        estado_model = EstadoCohorteEstablecimiento
        return_url = 'cohortesEstablecimientoIndex'
    elif tipo_unidad_educativa == 'anexo':
        cohorte_unidad_educativa = CohorteAnexo.objects.get(pk=cohorte_ue_id, anexo__ambito__path__istartswith=request.get_perfil().ambito.path)
        unidad_educativa = cohorte_unidad_educativa.anexo
        estado_model = EstadoCohorteAnexo
        return_url = 'cohortesAnexoIndex'
    elif tipo_unidad_educativa == 'extension_aulica':
        cohorte_unidad_educativa = CohorteExtensionAulica.objects.get(pk=cohorte_ue_id, extension_aulica__ambito__path__istartswith=request.get_perfil().ambito.path)
        unidad_educativa = cohorte_unidad_educativa.extension_aulica
        estado_model = EstadoCohorteExtensionAulica
        return_url = 'cohortesExtensionAulicaIndex'

    cohorte_unidad_educativa.estado = estado_model.objects.get(nombre=estado_model.RECHAZADA)
    cohorte_unidad_educativa.save()
    cohorte_unidad_educativa.registrar_estado()

    request.set_flash('success', 'Los datos fueron actualizados correctamente.')

    return HttpResponseRedirect(reverse(return_url, args=[unidad_educativa.id]))


@login_required
#@credential_required('tit_cohorte_seguimiento')
def seguimiento(request, cohorte_ue_id, tipo_unidad_educativa):
    """
    Seguimiento de cohorte de la unidad educativa
    """
    if tipo_unidad_educativa == 'establecimiento':
        cohorte_unidad_educativa = CohorteEstablecimiento.objects.get(pk=cohorte_ue_id)
        objects = cohorte_unidad_educativa.seguimiento.all().order_by('anio')
        unidad_educativa = Establecimiento.objects.get(pk=cohorte_unidad_educativa.establecimiento.id, ambito__path__istartswith=request.get_perfil().ambito.path)
    elif tipo_unidad_educativa == 'anexo':
        cohorte_unidad_educativa = CohorteAnexo.objects.get(pk=cohorte_ue_id)
        objects = cohorte_unidad_educativa.seguimiento.all().order_by('anio')
        unidad_educativa = Anexo.objects.get(pk=cohorte_unidad_educativa.anexo.id, ambito__path__istartswith=request.get_perfil().ambito.path)
    elif tipo_unidad_educativa == 'extension_aulica':
        cohorte_unidad_educativa = CohorteExtensionAulica.objects.get(pk=cohorte_ue_id)
        objects = cohorte_unidad_educativa.seguimiento.all().order_by('anio')
        unidad_educativa = ExtensionAulica.objects.get(pk=cohorte_unidad_educativa.extension_aulica.id, ambito__path__istartswith=request.get_perfil().ambito.path)
    else:
        raise Exception('Tipo de unidad educativa erróneo.')
        
    return my_render(request, 'titulos/cohorte/seguimiento/seguimiento.html', {
        'objects': objects,
        'cohorte_unidad_educativa': cohorte_unidad_educativa,
        'tipo_unidad_educativa': tipo_unidad_educativa,
        'unidad_educativa': unidad_educativa,
    })


@login_required
#@credential_required('tit_cohorte_seguimiento')
def create(request, cohorte_ue_id, tipo_unidad_educativa):

    if tipo_unidad_educativa == 'establecimiento':
        cohorte_unidad_educativa = CohorteEstablecimiento.objects.get(pk=cohorte_ue_id)
        unidad_educativa = Establecimiento.objects.get(pk=cohorte_unidad_educativa.establecimiento.id, ambito__path__istartswith=request.get_perfil().ambito.path)
        form_model = CohorteEstablecimientoSeguimientoForm
    elif tipo_unidad_educativa == 'anexo':
        cohorte_unidad_educativa = CohorteAnexo.objects.get(pk=cohorte_ue_id)
        unidad_educativa = Anexo.objects.get(pk=cohorte_unidad_educativa.anexo.id, ambito__path__istartswith=request.get_perfil().ambito.path)
        form_model = CohorteAnexoSeguimientoForm
    elif tipo_unidad_educativa == 'extension_aulica':
        cohorte_unidad_educativa = CohorteExtensionAulica.objects.get(pk=cohorte_ue_id)
        unidad_educativa = ExtensionAulica.objects.get(pk=cohorte_unidad_educativa.extension_aulica.id, ambito__path__istartswith=request.get_perfil().ambito.path)
        form_model = CohorteExtensionAulicaSeguimientoForm
    else:
        raise Exception('Tipo de unidad educativa erróneo.')

    if not cohorte_unidad_educativa.registrada():  # No aceptada
        request.set_flash('warning', 'No se puede generar años de seguimiento a cohortes no aceptadas.')
        return HttpResponseRedirect(reverse('cohorteSeguimientoIndex'))
    
    if request.method == 'POST':
        form = form_model(request.POST, cohorte_unidad_educativa=cohorte_unidad_educativa)
        if form.is_valid():
            seguimiento = form.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('cohorteSeguimiento', args=[tipo_unidad_educativa, cohorte_ue_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = form_model(cohorte_unidad_educativa=cohorte_unidad_educativa)

    return my_render(request, 'titulos/cohorte/seguimiento/new.html', {
        'form': form,
        'cohorte_unidad_educativa': cohorte_unidad_educativa,
        'cohorte': cohorte_unidad_educativa.cohorte,
        'tipo_unidad_educativa': tipo_unidad_educativa,
        'unidad_educativa': unidad_educativa,
    })
    
    
@login_required
#@credential_required('tit_cohorte_seguimiento')
def edit(request, seguimiento_id, tipo_unidad_educativa):
    
    if tipo_unidad_educativa == 'establecimiento':
        seguimiento = CohorteEstablecimientoSeguimiento.objects.get(pk=seguimiento_id)
        cohorte_unidad_educativa = seguimiento.cohorte_establecimiento
        unidad_educativa = Establecimiento.objects.get(pk=cohorte_unidad_educativa.establecimiento.id, ambito__path__istartswith=request.get_perfil().ambito.path)
        form_model = CohorteEstablecimientoSeguimientoForm
    elif tipo_unidad_educativa == 'anexo':
        seguimiento = CohorteAnexoSeguimiento.objects.get(pk=seguimiento_id)
        cohorte_unidad_educativa = seguimiento.cohorte_anexo
        unidad_educativa = Anexo.objects.get(pk=cohorte_unidad_educativa.anexo.id, ambito__path__istartswith=request.get_perfil().ambito.path)
        form_model = CohorteAnexoSeguimientoForm
    elif tipo_unidad_educativa == 'extension_aulica':
        seguimiento = CohorteExtensionAulicaSeguimiento.objects.get(pk=seguimiento_id)
        cohorte_unidad_educativa = seguimiento.cohorte_extension_aulica
        unidad_educativa = ExtensionAulica.objects.get(pk=cohorte_unidad_educativa.extension_aulica.id, ambito__path__istartswith=request.get_perfil().ambito.path)
        form_model = CohorteExtensionAulicaSeguimientoForm
    else:
        raise Exception('Tipo de unidad educativa erróneo.')

    if not cohorte_unidad_educativa.registrada():  # No aceptada
        request.set_flash('warning', 'No se puede generar años de seguimiento a cohortes no aceptadas.')
        return HttpResponseRedirect(reverse('cohorteSeguimientoIndex'))

    if request.method == 'POST':
        form = form_model(request.POST, instance=seguimiento, cohorte_unidad_educativa=cohorte_unidad_educativa)
        if form.is_valid():
            seguimiento = form.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('cohorteSeguimiento', args=[tipo_unidad_educativa, cohorte_unidad_educativa.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = form_model(instance=seguimiento, cohorte_unidad_educativa=cohorte_unidad_educativa)

    return my_render(request, 'titulos/cohorte/seguimiento/edit.html', {
        'form': form,
        'cohorte_unidad_educativa': cohorte_unidad_educativa,
        'cohorte': cohorte_unidad_educativa.cohorte,
        'tipo_unidad_educativa': tipo_unidad_educativa,
        'unidad_educativa': unidad_educativa,
    })


@login_required
#@credential_required('tit_cohorte_seguimiento')
def delete(request, seguimiento_id, tipo_unidad_educativa):
    """
    Eliminación de año de seguimiento de cohorte
    """
    if tipo_unidad_educativa == 'establecimiento':
        seguimiento = CohorteEstablecimientoSeguimiento.objects.get(pk=seguimiento_id)
        cohorte_unidad_educativa = seguimiento.cohorte_establecimiento
        unidad_educativa = Establecimiento.objects.get(pk=cohorte_unidad_educativa.establecimiento.id, ambito__path__istartswith=request.get_perfil().ambito.path)
    elif tipo_unidad_educativa == 'anexo':
        seguimiento = CohorteAnexoSeguimiento.objects.get(pk=seguimiento_id)
        cohorte_unidad_educativa = seguimiento.cohorte_anexo
        unidad_educativa = Anexo.objects.get(pk=cohorte_unidad_educativa.anexo.id, ambito__path__istartswith=request.get_perfil().ambito.path)
    elif tipo_unidad_educativa == 'extension_aulica':
        seguimiento = CohorteExtensionAulicaSeguimiento.objects.get(pk=seguimiento_id)
        cohorte_unidad_educativa = seguimiento.cohorte_extension_aulica
        unidad_educativa = ExtensionAulica.objects.get(pk=cohorte_unidad_educativa.extension_aulica.id, ambito__path__istartswith=request.get_perfil().ambito.path)

    if request.method == 'POST':
        seguimiento.delete()
        request.set_flash('success', 'El año de seguimiento fue eliminado correctamente.')
        """ Redirecciono para evitar el reenvío del form """
        return HttpResponseRedirect(reverse('cohorteSeguimiento', args=[tipo_unidad_educativa, cohorte_unidad_educativa.id]))
    else:
        request.set_flash('warning', 'Está seguro de eliminar el año de seguimiento? Esta operación no puede deshacerse.')
        
    return my_render(request, 'titulos/cohorte/seguimiento/delete.html', {
        'seguimiento': seguimiento,
        'tipo_unidad_educativa': tipo_unidad_educativa,
        'cohorte_unidad_educativa': cohorte_unidad_educativa,
    })
