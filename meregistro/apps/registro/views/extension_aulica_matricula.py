# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.EstadoExtensionAulica import EstadoExtensionAulica
from apps.registro.models.ExtensionAulicaMatricula import ExtensionAulicaMatricula
from apps.registro.forms.ExtensionAulicaMatriculaForm import ExtensionAulicaMatriculaForm
from apps.registro.forms.ExtensionAulicaMatriculaFormFilters import ExtensionAulicaMatriculaFormFilters
from apps.backend.models import ConfiguracionSolapasExtensionAulica
from apps.registro.forms.VerificacionDatosExtensionAulicaForm import VerificacionDatosExtensionAulicaForm

ITEMS_PER_PAGE = 50

@login_required
def __extension_aulica_dentro_del_ambito(request, extension_aulica):
    """
    El extension_aulica está dentro del ámbito?
    """
    try:
        extension_aulica = ExtensionAulica.objects.get(id=extension_aulica.id, ambito__path__istartswith=request.get_perfil().ambito.path)
    except extension_aulica.DoesNotExist:
        return False
    return True

@login_required
def __get_extension_aulica(request, extension_aulica_id):    
    extension_aulica = ExtensionAulica.objects.get(pk=extension_aulica_id)
    if not __extension_aulica_dentro_del_ambito(request, extension_aulica):
        raise Exception('El extension_aulica no se encuentra en su ámbito.')
    return extension_aulica



@login_required
@credential_required('reg_extension_aulica_modificar')
def index(request, extension_aulica_id):
    extension_aulica = __get_extension_aulica(request, extension_aulica_id)
    """
    Búsqueda de extension_aulicas
    """
    if request.method == 'GET':
        form_filter = ExtensionAulicaMatriculaFormFilters(request.GET, extension_aulica_id=extension_aulica.id)
    else:
        form_filter = ExtensionAulicaFormFilters(extension_aulica_id=extension_aulica.id)
    q = build_query(form_filter, 1, request)
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

    return my_render(request, 'registro/extension_aulica/matricula/index.html', {
        'extension_aulica': extension_aulica,
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'verificado': extension_aulica.get_verificacion_datos().matricula,
        'datos_verificados': extension_aulica.get_verificacion_datos().get_datos_verificados(),
        'configuracion_solapas': ConfiguracionSolapasExtensionAulica.get_instance(),
        'current_page': 'matricula',
        'form_verificacion': VerificacionDatosExtensionAulicaForm(
			dato_verificacion='matricula', 
			unidad_educativa_id=extension_aulica.id, 
			return_url='extensionAulicaMatriculaIndex', 
			verificado=extension_aulica.get_verificacion_datos().matricula),
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('anio')


@login_required
@credential_required('reg_extension_aulica_modificar')
def create(request, extension_aulica_id):
    extension_aulica = __get_extension_aulica(request, extension_aulica_id)
    """
    Alta de matricula.
    """

    if request.method == 'POST':
        form = ExtensionAulicaMatriculaForm(request.POST, extension_aulica=extension_aulica)
        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.extension_aulica_id = extension_aulica.id
            matricula.set_formacion_continua()
            matricula.set_formacion_docente()
            matricula.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('extensionAulicaMatriculaIndex', args=[matricula.extension_aulica_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = ExtensionAulicaMatriculaForm(extension_aulica=extension_aulica)
    return my_render(request, 'registro/extension_aulica/matricula/new.html', {
        'extension_aulica': extension_aulica,
        'form': form,
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def edit(request, matricula_id):
    """
    Edición de los datos de una matricula.
    """
    matricula = ExtensionAulicaMatricula.objects.get(pk=matricula_id)
    extension_aulica = __get_extension_aulica(request, matricula.extension_aulica_id)

    if request.method == 'POST':
        form = ExtensionAulicaMatriculaForm(request.POST, instance=matricula, extension_aulica=extension_aulica)
        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.set_formacion_continua()
            matricula.set_formacion_docente()
            matricula.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('extensionAulicaMatriculaIndex', args=[matricula.extension_aulica_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = ExtensionAulicaMatriculaForm(instance=matricula, extension_aulica=extension_aulica)

    return my_render(request, 'registro/extension_aulica/matricula/edit.html', {
        'form': form,
        'matricula': matricula,
        'extension_aulica': extension_aulica,
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def delete(request, matricula_id):
    matricula = ExtensionAulicaMatricula.objects.get(pk=matricula_id)
    extension_aulica = __get_extension_aulica(request, matricula.extension_aulica_id)
    
    matricula.delete()
    request.set_flash('success', 'Datos del matricula eliminados correctamente.')
    return HttpResponseRedirect(reverse('extensionAulicaMatriculaIndex', args=[matricula.extension_aulica_id]))
