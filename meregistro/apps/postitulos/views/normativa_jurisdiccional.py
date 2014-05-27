# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import NormativaJurisdiccional, EstadoNormativaJurisdiccional
from apps.postitulos.forms import NormativaPostituloJurisdiccionalFormFilters, NormativaPostituloJurisdiccionalForm
from apps.registro.models import Jurisdiccion
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
from apps.reportes.views.normativa_jurisdiccional import normativas_jurisdiccionales as reporte_normativas_jurisdiccionales
from apps.reportes.models import Reporte

ITEMS_PER_PAGE = 50


def build_query(filters, page, request):
    "Construye el query de búsqueda a partir de los filtros."
    return filters.buildQuery().order_by('id').filter(jurisdiccion = request.get_perfil().jurisdiccion())


@login_required
@credential_required('tit_nor_jur_consulta')
def index(request):
    " Búsqueda de orientaciones "
    if request.method == 'GET':
        form_filter = NormativaPostituloJurisdiccionalFormFilters(request.GET)
    else:
        form_filter = NormativaPostituloJurisdiccionalFormFilters()
    q = build_query(form_filter, 1, request)

    if 'export' in request.GET:
	    return reporte_normativas_jurisdiccionales(request, q)

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
    return my_render(request, 'postitulos/normativa_jurisdiccional/index.html', {
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
		'export_url': Reporte.build_export_url(request.build_absolute_uri()),
    })


@login_required
#@credential_required('tit_nor_jur_alta')
def create(request):
    " Crear nueva normativa "

    if request.method == 'POST':
        form = NormativaJurisdiccionalForm(request.POST)
        if form.is_valid():
            normativa_jurisdiccional = form.save(commit = False)
            normativa_jurisdiccional.jurisdiccion = request.get_perfil().jurisdiccion()
            normativa_jurisdiccional.save()

            normativa_jurisdiccional.registrar_estado()

            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('normativaJurisdiccionalEdit', args = [normativa_jurisdiccional.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = NormativaJurisdiccionalForm()

    return my_render(request, 'titulos/normativa_jurisdiccional/new.html', {
        'form': form,
        'is_new': True,
    })


@login_required
#@credential_required('tit_nor_jur_modificar')
def edit(request, normativa_jurisdiccional_id):
    " Edición de los datos de una normativa jurisdiccional "
    normativa_jurisdiccional = NormativaJurisdiccional.objects.get(pk = normativa_jurisdiccional_id)

    estado_actual = normativa_jurisdiccional.estado
    if estado_actual is None:
        estado_actual_id = None
    else:
        estado_actual_id = estado_actual.id

    if request.method == 'POST':
        form = NormativaJurisdiccionalForm(request.POST, instance = normativa_jurisdiccional, initial = {'estado': estado_actual_id})
        if form.is_valid():
            normativa_jurisdiccional = form.save()

            "Cambiar el estado?"
            if int(request.POST['estado']) is not estado_actual_id:
                normativa_jurisdiccional.registrar_estado()

            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('normativaJurisdiccionalEdit', args = [normativa_jurisdiccional_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = NormativaJurisdiccionalForm(instance = normativa_jurisdiccional, initial = {'estado': estado_actual_id})

        form.fields['estado'].empty_label = None
    return my_render(request, 'titulos/normativa_jurisdiccional/edit.html', {
        'form': form,
        'is_new': False,
    })


@login_required
#@credential_required('tit_nor_jur_eliminar')
def eliminar(request, normativa_jurisdiccional_id):
    """
    Eliminación de una normativa
    --- mientras no sea referida por un título jurisdiccional ---
    """
    normativa_jurisdiccional = NormativaJurisdiccional.objects.get(pk = normativa_jurisdiccional_id)

    puede_eliminarse = normativa_jurisdiccional.puede_eliminarse()
    if not puede_eliminarse:
        request.set_flash('warning', 'La normativa no puede eliminarse porque tiene datos asociados.')
    else:
        request.set_flash('warning', '¿Está seguro de eliminar la normativa? Esta operación no puede deshacerse.')

    if request.method == 'POST':
        normativa_jurisdiccional.delete()
        request.set_flash('success', 'La normativa fue eliminada correctamente.')
        """ Redirecciono para evitar el reenvío del form """
        return HttpResponseRedirect(reverse('normativaJurisdiccional'))
    return my_render(request, 'titulos/normativa_jurisdiccional/eliminar.html', {
        'normativa_jurisdiccional_id': normativa_jurisdiccional.id,
        'puede_eliminarse': puede_eliminarse,
    })


@login_required
#@credential_required('revisar_jurisdiccion')
def revisar_jurisdiccion(request, oid):
    o = NormativaJurisdiccional.objects.get(pk = oid)
    o.revisado_jurisdiccion = True
    o.save()
    request.set_flash('success', 'Registro revisado.')
    return HttpResponseRedirect(reverse('normativaJurisdiccional'))
