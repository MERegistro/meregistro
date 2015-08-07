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
@credential_required('registro_certificar_carga')
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
@credential_required('registro_certificar_carga')
def certificar_establecimiento(request, anio, establecimiento_id):
    if not anio in ANIOS_HABILITADOS:
        request.set_flash('warning', 'No es posible certificar la carga del año ' + str(anio) + '.')
        return HttpResponseRedirect(reverse('certificacionCargaIndex', args=[anio]))

    establecimiento = Establecimiento.objects.get(id=establecimiento_id, ambito__path=request.get_perfil().ambito.path)
    
    if establecimiento.carga_certificada(anio):
        request.set_flash('warning', 'La carga del año ' + str(anio) + ' ya se encuentra certificada.')
        return HttpResponseRedirect(reverse('certificacionCargaIndex', args=[anio]))
        
    if request.method == 'POST':
        certificacion = establecimiento.certificar_carga(anio, request.get_perfil().usuario)
        request.set_flash('success', 'Carga del año ' + str(anio) + ' certificada correctamente.')
        MailHelper.notify_by_email(MailHelper.CERTIFICACION_CARGA_ESTABLECIMIENTO, certificacion)
        return HttpResponseRedirect(reverse('certificacionCargaIndex', args=[anio]))
        
    return my_render(request, 'registro/certificacion_carga/certificar_establecimiento.html', {
        'anio': anio,
        'establecimiento': establecimiento,
        'puede_certificar_carga': establecimiento.puede_certificar_carga(anio)
    })


@login_required
@credential_required('registro_certificar_carga')
def certificar_anexo(request, anio, anexo_id):
    if not anio in ANIOS_HABILITADOS:
        request.set_flash('warning', 'No es posible certificar la carga del año ' + str(anio) + '.')
        return HttpResponseRedirect(reverse('certificacionCargaIndex', args=[anio]))

    anexo = Anexo.objects.get(id=anexo_id, ambito__path__istartswith=request.get_perfil().ambito.path)
    
    if anexo.carga_certificada(anio):
        request.set_flash('warning', 'La carga del año ' + str(anio) + ' ya se encuentra certificada.')
        return HttpResponseRedirect(reverse('certificacionCargaIndex', args=[anio]))
        
    if request.method == 'POST':
        certificacion = anexo.certificar_carga(anio, request.get_perfil().usuario)
        request.set_flash('success', 'Carga del año ' + str(anio) + ' certificada correctamente.')
        MailHelper.notify_by_email(MailHelper.CERTIFICACION_CARGA_ANEXO, certificacion)
        return HttpResponseRedirect(reverse('certificacionCargaIndex', args=[anio]))
        
    return my_render(request, 'registro/certificacion_carga/certificar_anexo.html', {
        'anio': anio,
        'anexo': anexo,
        'puede_certificar_carga': anexo.puede_certificar_carga(anio)
    })


@login_required
@credential_required('registro_certificar_carga')
def certificar_extension_aulica(request, anio, extension_aulica_id):
    if not anio in ANIOS_HABILITADOS:
        request.set_flash('warning', 'No es posible certificar la carga del año ' + str(anio) + '.')
        return HttpResponseRedirect(reverse('certificacionCargaIndex', args=[anio]))

    extension_aulica = ExtensionAulica.objects.get(id=extension_aulica_id, ambito__path__istartswith=request.get_perfil().ambito.path)
    
    if extension_aulica.carga_certificada(anio):
        request.set_flash('warning', 'La carga del año ' + str(anio) + ' ya se encuentra certificada.')
        return HttpResponseRedirect(reverse('certificacionCargaIndex', args=[anio]))
        
    if request.method == 'POST':
        certificacion = extension_aulica.certificar_carga(anio, request.get_perfil().usuario)
        request.set_flash('success', 'Carga del año ' + str(anio) + ' certificada correctamente.')
        MailHelper.notify_by_email(MailHelper.CERTIFICACION_CARGA_EXTENSION_AULICA, certificacion)
        return HttpResponseRedirect(reverse('certificacionCargaIndex', args=[anio]))
        
    return my_render(request, 'registro/certificacion_carga/certificar_extension_aulica.html', {
        'anio': anio,
        'extension_aulica': extension_aulica,
        'puede_certificar_carga': extension_aulica.puede_certificar_carga(anio)
    })
