# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Rol
from apps.seguridad.forms import RolFormFilters, RolForm
from django.core.paginator import Paginator

ITEMS_PER_PAGE = 50


@credential_required('seg_rol_registrar')
def index(request):
    """
    Búsqueda de roles
    """
    if request.method == 'GET':
        form_filter = RolFormFilters(request.GET)
    else:
        form_filter = RolFormFilters()
    q = build_query(form_filter, 1)
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

    return my_render(request, 'seguridad/rol/index.html', {
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1
    })


def build_query(filters, page):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('descripcion')


@credential_required('seg_rol_registrar')
def create(request):
    """
    Alta de rol.
    """
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            rol = form.save()
            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('rolEdit', args=[rol.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = RolForm()

    return my_render(request, 'seguridad/rol/new.html', {
        'form': form,
        'is_new': True,
    })


@credential_required('seg_rol_registrar')
def edit(request, rol_id):
    """
    Edición de los datos de un rol.
    """
    rol = Rol.objects.get(pk=rol_id)
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            rol = form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = RolForm(instance=rol)
    return my_render(request, 'seguridad/rol/edit.html', {
        'form': form,
        'rol': rol,
    })


@credential_required('reg_rol_registrar')
def delete(request, rol_id):
    rol = Rol.objects.get(pk=rol_id)

    if rol.perfil.count() > 0:
        request.set_flash('warning', 'No se puede eliminar la dependencia funcional porque tiene establecimientos asociados.')
    else:
        rol.delete()
        request.set_flash('success', 'Registro eliminado correctamente.')

    return HttpResponseRedirect(reverse('rol'))
