# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import CohorteAnexo, EstadoCohorteAnexo, CohorteAnexoSeguimiento, EstadoTituloJurisdiccional
from apps.titulos.forms import AceptarCohorteAnexoFormFilters, CohorteAnexoConfirmarForm, CohorteAnexoSeguimientoForm
from apps.registro.models import Anexo
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
import datetime

ITEMS_PER_PAGE = 50


def __flat_list(list_to_flat):
    # Método para aplanar las listas
    return [i for j in list_to_flat for i in j]


def __get_anexo_actual(request):
    """
    Trae el único anexo que tiene asignado el usuario actual
    """
    try:
        return Anexo.objects.get(ambito__id=request.get_perfil().ambito.id)
    except Anexo.DoesNotExist:
		raise Exception('ERROR: El usuario no tiene asignado un anexo.')


def build_confirmar_cohortes_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    anexo = __get_anexo_actual(request)
    estado = EstadoTituloJurisdiccional.objects.get(nombre=EstadoTituloJurisdiccional.CONTROLADO)
    # Filtra que el año de la última cohorte sea menor o igual al año en curso y el estado sea controlado
    return filters.buildQuery().filter(anexo=anexo, cohorte__titulo_jurisdiccional__estado__nombre=estado, \
        cohorte__titulo_jurisdiccional__datos_cohorte__anio_ultima_cohorte__gte=datetime.date.today().year).order_by('cohorte__titulo_jurisdiccional__titulo__nombre', '-cohorte__anio')


@login_required
#@credential_required('tit_cohorte_aceptar_asignacion')
def index(request):
    """
    Index de cohorte establecimiento
    """
    anexo = __get_anexo_actual(request)

    if request.method == 'GET':
        form_filter = AceptarCohorteAnexoFormFilters(request.GET)
    else:
        form_filter = AceptarCohorteAnexoFormFilters()
    q = build_confirmar_cohortes_query(form_filter, 1, request)

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
    return my_render(request, 'titulos/cohorte/cohorte_anexo/index.html', {
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1
    })


@login_required
#@credential_required('tit_cohorte_aceptar_asignacion')
def confirmar(request, cohorte_anexo_id):
    """
    Confirmar cohorte
    """
    cohorte_anexo = CohorteAnexo.objects.get(pk=cohorte_anexo_id)

    if request.method == 'POST':
        form = CohorteAnexoConfirmarForm(request.POST, instance=cohorte_anexo)
        if form.is_valid():
            cohorte_anexo = form.save(commit=False)
            estado = EstadoCohorteAnexo.objects.get(nombre=EstadoCohorteAnexo.ACEPTADA)
            cohorte_anexo.estado = estado
            cohorte_anexo.save()
            cohorte_anexo.registrar_estado()

            request.set_flash('success', 'La cohorte fue confirmada correctamente.')
            """ Redirecciono para evitar el reenvío del form """
            return HttpResponseRedirect(reverse('cohorteAnexoIndex'))

        else:
            request.set_flash('warning', 'Ocurrió un error confirmando la cohorte.')
    else:
        form = CohorteAnexoConfirmarForm(instance=cohorte_anexo)

    return my_render(request, 'titulos/cohorte/cohorte_anexo/confirmar.html', {
        'cohorte_anexo': cohorte_anexo,
        'cohorte': cohorte_anexo.cohorte,
        'form': form,
    })


@login_required
#@credential_required('tit_cohorte_seguimiento')
def seguimiento(request, cohorte_anexo_id):
    """
    Seguimiento de cohorte anexo
    """
    anexo = __get_anexo_actual(request)
    cohorte_anexo = CohorteAnexo.objects.get(pk=cohorte_anexo_id)

    if cohorte_anexo.inscriptos is None:  # No aceptada
        request.set_flash('warning', 'No se puede generar años de seguimiento a cohortes no aceptadas.')
        return HttpResponseRedirect(reverse('cohorteAnexoIndex'))

    objects = CohorteAnexoSeguimiento.objects.filter(cohorte_anexo=cohorte_anexo).order_by('anio')
    return my_render(request, 'titulos/cohorte/cohorte_anexo/seguimiento.html', {
        'objects': objects,
        'cohorte_anexo': cohorte_anexo,
        'page_title': 'Seguimiento de cohote',
        'actual_page': 'seguimiento',
    })


@login_required
#@credential_required('tit_cohorte_seguimiento')
def create_seguimiento(request, cohorte_anexo_id):

    cohorte_anexo = CohorteAnexo.objects.get(pk=cohorte_anexo_id)

    if cohorte_anexo.inscriptos is None:  # No aceptada
        request.set_flash('warning', 'No se puede generar años de seguimiento a cohortes no aceptadas.')
        return HttpResponseRedirect(reverse('cohorteAnexoSeguimiento', args=[cohorte_anexo.id]))

    if request.method == 'POST':
        form = CohorteAnexoSeguimientoForm(request.POST, inscriptos_total=cohorte_anexo.inscriptos, anio_cohorte=cohorte_anexo.cohorte.anio, cohorte_anexo_id=cohorte_anexo.id)
        if form.is_valid():
            seguimiento = form.save(commit=False)
            seguimiento.cohorte_anexo = cohorte_anexo
            seguimiento.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('cohorteAnexoSeguimiento', args=[cohorte_anexo.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = CohorteAnexoSeguimientoForm(inscriptos_total=cohorte_anexo.inscriptos, anio_cohorte=cohorte_anexo.cohorte.anio, cohorte_anexo_id=cohorte_anexo.id)

    return my_render(request, 'titulos/cohorte/cohorte_anexo/new.html', {
        'form': form,
        'cohorte_anexo': cohorte_anexo,
        'form_template': 'titulos/cohorte/cohorte_anexo/form_seguimiento.html',
        'page_title': 'Datos de seguimiento',
        'actual_page': 'datos_seguimiento',
    })


@login_required
#@credential_required('tit_cohorte_seguimiento')
def edit_seguimiento(request, seguimiento_id):
    """
    Confirmar cohorte
    """
    seguimiento = CohorteAnexoSeguimiento.objects.get(pk=seguimiento_id)
    cohorte_anexo = seguimiento.cohorte_anexo

    if request.method == 'POST':
        form = CohorteAnexoSeguimientoForm(request.POST, instance=seguimiento, inscriptos_total=cohorte_anexo.inscriptos, anio_cohorte=cohorte_anexo.cohorte.anio, cohorte_anexo_id=cohorte_anexo.id)
        if form.is_valid():
            seguimiento = form.save(commit=False)
            seguimiento.cohorte_anexo = cohorte_anexo
            seguimiento.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('cohorteAnexoSeguimiento', args=[cohorte_anexo.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = CohorteAnexoSeguimientoForm(instance=seguimiento, inscriptos_total=cohorte_anexo.inscriptos, anio_cohorte=cohorte_anexo.cohorte.anio, cohorte_anexo_id=cohorte_anexo.id)

    return my_render(request, 'titulos/cohorte/cohorte_anexo/edit.html', {
        'form': form,
        'cohorte_anexo': cohorte_anexo,
        'form_template': 'titulos/cohorte/cohorte_anexo/form_seguimiento.html',
        'page_title': 'Datos de seguimiento',
        'actual_page': 'datos_seguimiento',
    })


@login_required
#@credential_required('tit_cohorte_seguimiento')
def eliminar(request, seguimiento_id):
    """
    Eliminación de año de seguimiento de cohorte
    """
    seguimiento = CohorteAnexoSeguimiento.objects.get(pk=seguimiento_id)

    if request.method == 'POST':
        if int(request.POST['seguimiento_id']) is not int(seguimiento.id):
            raise Exception('Error en la consulta!')

        seguimiento.delete()
        request.set_flash('success', 'El año de seguimiento fue eliminado correctamente.')
        """ Redirecciono para evitar el reenvío del form """
        return HttpResponseRedirect(reverse('cohorteAnexoSeguimiento', args=[seguimiento.cohorte_anexo.id]))
    else:
        request.set_flash('warning', 'Está seguro de eliminar el año de seguimiento? Esta operación no puede deshacerse.')
    return my_render(request, 'titulos/cohorte/cohorte_anexo/eliminar.html', {
        'seguimiento_id': seguimiento.id,
    })
