# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models import DependenciaFuncional, TipoDependenciaFuncional, TipoGestion
from apps.registro.forms import DependenciaFuncionalFormFilters, DependenciaFuncionalForm
from apps.registro.models import Jurisdiccion
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
from apps.reportes.views.dependencia_funcional import dependencias_funcionales as reporte_dependencias_funcionales
from apps.reportes.models import Reporte

ITEMS_PER_PAGE = 50


@login_required
@credential_required('reg_df_consulta')
def index(request):
    """
    Búsqueda de dependencias
    """
    if request.method == 'GET':
        form_filter = DependenciaFuncionalFormFilters(request.GET)
    else:
        form_filter = DependenciaFuncionalFormFilters()
    q = build_query(form_filter, 1)
    q = q.filter(ambito__path__istartswith=request.get_perfil().ambito.path)

    try:
        if request.GET['export'] == '1':
            return reporte_dependencias_funcionales(request, q)
    except KeyError:
        pass

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
    if request.get_perfil().jurisdiccion() is not None:
        form_filter.fields['jurisdiccion'].queryset = Jurisdiccion.objects.filter(id=request.get_perfil().jurisdiccion().id)

    return my_render(request, 'registro/dependencia_funcional/index.html', {
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


def build_query(filters, page):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('nombre')


@login_required
@credential_required('reg_df_consulta')
def create(request):
    """
    Alta de dependencia.
    """
    if request.method == 'POST':
        form = DependenciaFuncionalForm(request.POST)
        if form.is_valid():
            dependencia_funcional = form.save(commit=True)

            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('dependenciaFuncionalEdit', args=[dependencia_funcional.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = DependenciaFuncionalForm()
    if request.get_perfil().jurisdiccion() is not None:
        form.fields['jurisdiccion'].queryset = Jurisdiccion.objects.filter(id=request.get_perfil().jurisdiccion().id)
    return my_render(request, 'registro/dependencia_funcional/new.html', {
        'form': form,
        'is_new': True,
    })


@login_required
@credential_required('reg_df_modificar')
def edit(request, dependencia_funcional_id):
    """
    Edición de los datos de una dependencia funcional.
    """
    dependencia_funcional = DependenciaFuncional.objects.get(pk=dependencia_funcional_id)
    if request.method == 'POST':
        form = DependenciaFuncionalForm(request.POST, instance=dependencia_funcional)
        if form.is_valid():
            dependencia_funcional = form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = DependenciaFuncionalForm(instance=dependencia_funcional)
    if request.get_perfil().jurisdiccion() is not None:
        form.fields['jurisdiccion'].queryset = Jurisdiccion.objects.filter(id=request.get_perfil().jurisdiccion().id)

    return my_render(request, 'registro/dependencia_funcional/edit.html', {
        'form': form,
        'dependencia_funcional': dependencia_funcional,
    })


@login_required
@credential_required('reg_df_baja')
def delete(request, dependencia_funcional_id):
    dependencia_funcional = DependenciaFuncional.objects.get(pk=dependencia_funcional_id)
    has_establecimientos = dependencia_funcional.hasEstablecimientos()

    # TODO: chequear que pertenece al ámbito
    if has_establecimientos:
        request.set_flash('warning', 'No se puede eliminar la dependencia funcional porque tiene establecimientos asociados.')
    else:
        dependencia_funcional.delete()
        request.set_flash('success', 'Registro eliminado correctamente.')

    return HttpResponseRedirect(reverse('dependenciaFuncional'))
