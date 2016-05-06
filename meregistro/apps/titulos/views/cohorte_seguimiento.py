# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import TipoAmbito
from apps.titulos.models import CohorteEstablecimiento, CohorteAnexo, CohorteExtensionAulica, EstadoCarreraJurisdiccional, \
    EstadoCohorteEstablecimiento, EstadoCohorteAnexo, EstadoCohorteExtensionAulica, \
    CohorteEstablecimientoSeguimiento, CohorteAnexoSeguimiento, CohorteExtensionAulicaSeguimiento
from apps.titulos.forms import CohortesUnidadEducativaFormFilters, CohorteEstablecimientoConfirmarForm,\
    CohorteAnexoConfirmarForm, CohorteExtensionAulicaConfirmarForm, \
    CohorteEstablecimientoSeguimientoForm, CohorteAnexoSeguimientoForm, CohorteExtensionAulicaSeguimientoForm
from apps.registro.models import Jurisdiccion, Establecimiento, Anexo, ExtensionAulica
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
import datetime

ITEMS_PER_PAGE = 50


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
@credential_required('tit_cohorte_seguimiento_consulta')
def index(request):
    tipo_perfil = request.get_perfil().ambito.tipo
    
    unidad_educativa = __get_ue_actual(request, tipo_perfil)
    
    if unidad_educativa.__class__ == Establecimiento:
        establecimiento = unidad_educativa
    elif unidad_educativa.__class__ == Anexo or unidad_educativa.__class__ == ExtensionAulica:
        establecimiento = unidad_educativa.establecimiento
    
    anexos = establecimiento.anexos
    extensiones_aulicas = establecimiento.extensiones_aulicas

    return my_render(request, 'titulos/cohorte/seguimiento/index.html', {
        'establecimiento': establecimiento,
        'anexos': anexos.all(),
        'extensiones_aulicas': extensiones_aulicas.all(),
        'unidad_educativa_actual': unidad_educativa,
        'tipo_perfil': tipo_perfil.nombre
    })


@login_required
#@credential_required('tit_cohorte_aceptar_asignacion')
def cohortes_unidad_educativa(request, unidad_educativa_id, tipo_unidad_educativa):
    """
    Index de cohorte unidad educativa
    """
    if tipo_unidad_educativa == 'establecimiento':
        unidad_educativa = Establecimiento.objects.get(pk=unidad_educativa_id, ambito__path__istartswith=request.get_perfil().ambito.path)
        titulo_interfaz = 'Seguimiento de Cohorte de la Sede'
    elif tipo_unidad_educativa == 'anexo':
        unidad_educativa = Anexo.objects.get(pk=unidad_educativa_id, ambito__path__istartswith=request.get_perfil().ambito.path)
        titulo_interfaz = 'Seguimiento de Cohorte del Anexo'
    elif tipo_unidad_educativa == 'extension_aulica':
        unidad_educativa = ExtensionAulica.objects.get(pk=unidad_educativa_id, ambito__path__istartswith=request.get_perfil().ambito.path)
        titulo_interfaz = 'Seguimiento de Cohorte de la Extensión Áulica'
        
    form_filter = CohortesUnidadEducativaFormFilters(request.GET, tipo_unidad_educativa=tipo_unidad_educativa)
        
    q = build_confirmar_cohortes_query(form_filter, 1, request, tipo_unidad_educativa, unidad_educativa_id)

    paginator = Paginator(q, ITEMS_PER_PAGE)

    try:
        page_number = int(request.GET['page'])
    except (KeyError, ValueError):
        page_number = 1
    # chequear los límites
    if page_number < 1:
        page_number = 1
    elif page_number > paginator.num_pages:
        page_number = paginator.num_pages

    page = paginator.page(page_number)
    objects = page.object_list
    return my_render(request, 'titulos/cohorte/seguimiento/cohortes_unidad_educativa.html', {
        'form_filters': form_filter,
        'objects': objects,
        'tipo_unidad_educativa': tipo_unidad_educativa,
        'unidad_educativa': unidad_educativa,
        'titulo_interfaz': titulo_interfaz,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1
    })



def build_confirmar_cohortes_query(filters, page, request, tipo_unidad_educativa, unidad_educativa_id):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    # Filtra que el año de la última cohorte sea menor o igual al año en curso y el estado sea controlado
    if tipo_unidad_educativa == 'establecimiento':
        return filters.buildQuery().filter(establecimiento__id=unidad_educativa_id)
    elif tipo_unidad_educativa == 'anexo':
        return filters.buildQuery().filter(anexo__id=unidad_educativa_id)
    elif tipo_unidad_educativa == 'extension_aulica':
        return filters.buildQuery().filter(extension_aulica__id=unidad_educativa_id)

    return filters.buildQuery()


@login_required
#@credential_required('tit_cohorte_aceptar_asignacion')
def confirmar(request, cohorte_ue_id, tipo_unidad_educativa):
    """
    Confirmar cohorte
    """
    if tipo_unidad_educativa == 'establecimiento':
        cohorte_unidad_educativa = CohorteEstablecimiento.objects.get(pk=cohorte_ue_id, establecimiento__ambito__path__istartswith=request.get_perfil().ambito.path)
        unidad_educativa = cohorte_unidad_educativa.establecimiento
        form_model = CohorteEstablecimientoConfirmarForm
        estado_model = EstadoCohorteEstablecimiento
        return_url = 'cohortesEstablecimientoIndex'
    elif tipo_unidad_educativa == 'anexo':
        cohorte_unidad_educativa = CohorteAnexo.objects.get(pk=cohorte_ue_id, anexo__ambito__path__istartswith=request.get_perfil().ambito.path)
        unidad_educativa = cohorte_unidad_educativa.anexo
        form_model = CohorteAnexoConfirmarForm
        estado_model = EstadoCohorteAnexo
        return_url = 'cohortesAnexoIndex'
    elif tipo_unidad_educativa == 'extension_aulica':
        cohorte_unidad_educativa = CohorteExtensionAulica.objects.get(pk=cohorte_ue_id, extension_aulica__ambito__path__istartswith=request.get_perfil().ambito.path)
        unidad_educativa = cohorte_unidad_educativa.extension_aulica
        form_model = CohorteExtensionAulicaConfirmarForm
        estado_model = EstadoCohorteExtensionAulica
        return_url = 'cohortesExtensionAulicaIndex'

    if request.method == 'POST':
        form = form_model(request.POST, instance=cohorte_unidad_educativa)
        if form.is_valid() and not cohorte_unidad_educativa.rechazada():
            cohorte_unidad_educativa = form.save(commit=False)
            estado = estado_model.objects.get(nombre=estado_model.REGISTRADA)
            cohorte_unidad_educativa.estado = estado
            cohorte_unidad_educativa.save()
            cohorte_unidad_educativa.registrar_estado()

            request.set_flash('success', 'Los datos fueron actualizados correctamente.')
            """ Redirecciono para evitar el reenvío del form """
            return HttpResponseRedirect(reverse(return_url, args=[unidad_educativa.id]))

        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = form_model(instance=cohorte_unidad_educativa)

    return my_render(request, 'titulos/cohorte/seguimiento/confirmar.html', {
        'cohorte_unidad_educativa': cohorte_unidad_educativa,
        'cohorte': cohorte_unidad_educativa.cohorte,
        'form': form,
        'unidad_educativa': unidad_educativa,
        'tipo_unidad_educativa': tipo_unidad_educativa,
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
#@credential_required('tit_cohorte_aceptar_asignacion')
def confirmar_finalizacion(request, cohorte_ue_id, tipo_unidad_educativa):
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

    if cohorte_unidad_educativa.estado.nombre != estado_model.FINALIZADA:
        cohorte_unidad_educativa.estado = estado_model.objects.get(nombre=estado_model.FINALIZADA)
        cohorte_unidad_educativa.save()
        cohorte_unidad_educativa.registrar_estado()
        request.set_flash('success', 'Se finalizó el seguimiento de la cohorte.')
    else:
        request.set_flash('warning', 'La cohorte ya se encuentra finalizada.')

    return HttpResponseRedirect(reverse(return_url, args=[unidad_educativa.id]))

@login_required
#@credential_required('tit_cohorte_aceptar_asignacion')
def finalizar_seguimiento(request, cohorte_ue_id, tipo_unidad_educativa):
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

    if request.method == 'POST':
        if cohorte_unidad_educativa.estado.nombre != estado_model.FINALIZADA:
            cohorte_unidad_educativa.estado = estado_model.objects.get(nombre=estado_model.FINALIZADA)
            cohorte_unidad_educativa.save()
            cohorte_unidad_educativa.registrar_estado()
            request.set_flash('success', 'Se finalizó el seguimiento de la cohorte.')
            return HttpResponseRedirect(reverse(return_url, args=[unidad_educativa.id]))
        else:
            request.set_flash('warning', 'La cohorte ya se encuentra finalizada.')
            return HttpResponseRedirect(reverse(return_url, args=[unidad_educativa.id]))

    return my_render(request, 'titulos/cohorte/seguimiento/finalizar_seguimiento.html', {
        'cohorte_unidad_educativa': cohorte_unidad_educativa,
        'unidad_educativa': unidad_educativa,
        'tipo_unidad_educativa': tipo_unidad_educativa,
    })

@login_required
#@credential_required('tit_cohorte_aceptar_asignacion')
def reactivar_seguimiento(request, cohorte_ue_id, tipo_unidad_educativa):
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

    if cohorte_unidad_educativa.estado.nombre == estado_model.FINALIZADA:
        cohorte_unidad_educativa.estado = estado_model.objects.get(nombre=estado_model.REGISTRADA)
        cohorte_unidad_educativa.save()
        cohorte_unidad_educativa.registrar_estado()
        request.set_flash('success', 'Se reactivó el seguimiento de la cohorte.')
    else:
        request.set_flash('warning', 'La cohorte no se finalizada.')

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
