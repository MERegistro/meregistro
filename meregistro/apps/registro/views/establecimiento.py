# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.TipoDominio import TipoDominio
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.models.EstablecimientoDomicilio import EstablecimientoDomicilio
from apps.registro.models.EstablecimientoInformacionEdilicia import EstablecimientoInformacionEdilicia
from apps.registro.models.EstablecimientoConexionInternet import EstablecimientoConexionInternet
from apps.registro.models.Localidad import Localidad
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento
from apps.registro.models.RegistroEstablecimiento import RegistroEstablecimiento
from apps.registro.forms.EstablecimientoFormFilters import EstablecimientoFormFilters
from apps.registro.forms.EstablecimientoForm import EstablecimientoForm
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
from apps.registro.forms.EstablecimientoCambiarEstadoForm import EstablecimientoCambiarEstadoForm
from apps.registro.forms.EstablecimientoDatosBasicosForm import EstablecimientoDatosBasicosForm
from apps.registro.forms.EstablecimientoNivelesForm import EstablecimientoNivelesForm
from apps.registro.forms.EstablecimientoTurnosForm import EstablecimientoTurnosForm
from apps.registro.forms.EstablecimientoFuncionesForm import EstablecimientoFuncionesForm
from apps.registro.forms.EstablecimientoDomicilioForm import EstablecimientoDomicilioForm
from apps.registro.forms.EstablecimientoInformacionEdiliciaForm import EstablecimientoInformacionEdiliciaForm
from apps.registro.forms.EstablecimientoConexionInternetForm import EstablecimientoConexionInternetForm
from apps.registro.FSMEstablecimiento import FSMEstablecimiento
from apps.registro.models import DependenciaFuncional

fsmEstablecimiento = FSMEstablecimiento()

ITEMS_PER_PAGE = 50


@login_required
@credential_required('reg_establecimiento_consulta')
def index(request):

    """
    Búsqueda de establecimientos
    """
    if request.method == 'GET':
        form_filter = EstablecimientoFormFilters(request.GET)
    else:
        form_filter = EstablecimientoFormFilters()
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

    if request.get_perfil().jurisdiccion() is not None:
        form_filter.fields['dependencia_funcional'].queryset = DependenciaFuncional.objects.filter(jurisdiccion = request.get_perfil().jurisdiccion())
    page = paginator.page(page_number)
    objects = page.object_list
    return my_render(request, 'registro/establecimiento/index.html', {
        'form_filters': form_filter,
        'objects': objects,
        'show_paginator': paginator.num_pages > 1,
        'has_prev': page.has_previous(),
        'has_next': page.has_next(),
        'page': page_number,
        'pages': paginator.num_pages,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('nombre').filter(ambito__path__istartswith = request.get_perfil().ambito.path)

@login_required
@credential_required('reg_establecimiento_nueva')
def create(request):
    """
    Alta de establecimiento.
    """
    if request.method == 'POST':
        form = EstablecimientoForm(request.POST)
        if form.is_valid():
            establecimiento = form.save()
            establecimiento.registrar_estado()

            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_CREATE, establecimiento)
            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('establecimientoEdit', args = [establecimiento.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = EstablecimientoForm()
    if request.get_perfil().jurisdiccion() is not None:
        form.fields['dependencia_funcional'].queryset = DependenciaFuncional.objects.filter(jurisdiccion = request.get_perfil().jurisdiccion())
    return my_render(request, 'registro/establecimiento/new.html', {
        'form': form,
        'is_new': True,
    })


@login_required
@credential_required('reg_establecimiento_modificar')
def edit(request, establecimiento_id):
    """
    Edición de los datos de un establecimiento.
    """
    establecimiento = Establecimiento.objects.get(pk = establecimiento_id)
    if request.method == 'POST':
        form = EstablecimientoForm(request.POST, instance = establecimiento)
        if form.is_valid():
            establecimiento = form.save()

            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoForm(instance = establecimiento)

    return my_render(request, 'registro/establecimiento/edit.html', {
        'form': form,
        'establecimiento': establecimiento,
    })


@login_required
@credential_required('reg_establecimiento_baja')
def delete(request, establecimiento_id):
    establecimiento = Establecimiento.objects.get(pk = establecimiento_id)
    has_anexos = establecimiento.hasAnexos()
    # TODO: chequear que pertenece al ámbito
    if has_anexos:
        request.set_flash('warning', 'No se puede eliminar el establecimiento porque tiene anexos asociados.')
    elif not establecimiento.isDeletable():
        request.set_flash('warning', 'El establecimiento no se puede eliminar.')
    else:
        establecimiento.delete()
        MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_DELETE, establecimiento)
        request.set_flash('success', 'Registro eliminado correctamente.')
    return HttpResponseRedirect(reverse('establecimiento'))


@login_required
@credential_required('reg_establecimiento_registrar')
def registrar(request, establecimientoId):
    """
    CU 23
    """
    establecimiento = Establecimiento.objects.get(pk = establecimientoId)
    form = __registrar_get_form(request, establecimiento)
    if request.method == 'POST' and __registrar_process(request, form, establecimiento):
            return HttpResponseRedirect(reverse('establecimiento'))
    return __registrar_show_form(request, form, establecimiento)

def __registrar_get_form(request, establecimiento):
    if request.method == 'POST':
        form = EstablecimientoCambiarEstadoForm(request.POST)
    else:
        form = EstablecimientoCambiarEstadoForm()
    form.fields["estado"].choices = map(lambda e: (e.id, e), fsmEstablecimiento.estadosDesde(establecimiento.estadoActual()))
    return form


def __registrar_show_form(request, form, establecimiento):
    return my_render(request, 'registro/establecimiento/registrar.html', {
        'form': form,
        'establecimiento': establecimiento
    })


def __registrar_process(request, form, establecimiento):
    if form.is_valid():
        nuevoEstado = form.cleaned_data['estado']
        try:
            establecimiento.registrar_estado(nuevoEstado, form.cleaned_data['observaciones'])
            request.set_flash('success', 'Establecimiento registrado correctamente.')
            return True
        except:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    return False


def __get_establecimiento_actual(request):
    """
    Trae el único establecimiento que tiene asignado, por ejemplo, un rector/director
    """
    try:
        establecimiento = Establecimiento.objects.get(ambito__id = request.get_perfil().ambito.id)
        if not bool(establecimiento):
            raise Exception('ERROR: El usuario no tiene asignado un establecimiento.')
        else:
            return establecimiento
    except Exception:
        pass

@login_required
@credential_required('reg_establecimiento_completar')
def completar_datos(request):
    """
    CU 26

    XXX: Por ahora no usamos esta vista, pero puede que más adelante la necesitemos
    para mostrar info del establecimiento
    """
    establecimiento = __get_establecimiento_actual(request)
    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'establecimiento': establecimiento,
    })

@login_required
@credential_required('reg_establecimiento_completar')
def completar_datos_basicos(request):
    """
    CU 26
    """
    establecimiento = __get_establecimiento_actual(request)
    if request.method == 'POST':
        form = EstablecimientoDatosBasicosForm(request.POST, instance = establecimiento)
        if form.is_valid():
            establecimiento = form.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoDatosBasicosForm(instance = establecimiento)

    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_datos_basicos.html',
        'establecimiento': establecimiento,
        'page_title': 'Datos básicos',
        'actual_page': 'datos_basicos',
    })

@login_required
@credential_required('reg_establecimiento_completar')
def completar_niveles(request):
    """
    CU 26
    """
    establecimiento = __get_establecimiento_actual(request)

    if request.method == 'POST':
        form = EstablecimientoNivelesForm(request.POST, instance = establecimiento)
        if form.is_valid():
            niveles = form.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoNivelesForm(instance = establecimiento)

    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_niveles.html',
        'establecimiento': establecimiento,
        'page_title': 'Niveles',
        'actual_page': 'niveles',
    })

@login_required
@credential_required('reg_establecimiento_completar')
def completar_turnos(request):
    """
    CU 26
    """
    establecimiento = __get_establecimiento_actual(request)

    if request.method == 'POST':
        form = EstablecimientoTurnosForm(request.POST, instance = establecimiento)
        if form.is_valid():
            turnos = form.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoTurnosForm(instance = establecimiento)

    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_turnos.html',
        'establecimiento': establecimiento,
        'page_title': 'Turnos',
        'actual_page': 'turnos',
    })

@login_required
@credential_required('reg_establecimiento_completar')
def completar_funciones(request):
    """
    CU 26
    """
    establecimiento = __get_establecimiento_actual(request)

    if request.method == 'POST':
        form = EstablecimientoFuncionesForm(request.POST, instance = establecimiento)
        if form.is_valid():
            funciones = form.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoFuncionesForm(instance = establecimiento)

    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_funciones.html',
        'establecimiento': establecimiento,
        'page_title': 'Funciones',
        'actual_page': 'funciones',
    })

@login_required
@credential_required('reg_establecimiento_completar')
def completar_domicilio(request):
    """
    CU 26
    """
    establecimiento = __get_establecimiento_actual(request)
    try:
        domicilio = establecimiento.domicilio.get()
    except:
        domicilio = EstablecimientoDomicilio()
        domicilio.establecimiento = establecimiento

    if request.method == 'POST':
        form = EstablecimientoDomicilioForm(request.POST, instance = domicilio)
        if form.is_valid():
            domicilio = form.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoDomicilioForm(instance = domicilio)

    jurisdiccion = request.get_perfil().jurisdiccion()
    form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id = jurisdiccion.id)

    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_domicilio.html',
        'establecimiento': establecimiento,
        'page_title': 'Domicilio',
        'actual_page': 'domicilio',
    })

@login_required
@credential_required('reg_establecimiento_completar')
def completar_informacion_edilicia(request):
    """
    CU 26
    """
    establecimiento = __get_establecimiento_actual(request)

    try:
        informacion_edilicia = EstablecimientoInformacionEdilicia.objects.get(establecimiento = establecimiento)
    except:
        informacion_edilicia = EstablecimientoInformacionEdilicia()
        informacion_edilicia.establecimiento = establecimiento

    if request.method == 'POST':
        form = EstablecimientoInformacionEdiliciaForm(request.POST, instance = informacion_edilicia)
        if form.is_valid():
            informacion_edilicia = form.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoInformacionEdiliciaForm(instance = informacion_edilicia)

    es_dominio_compartido_id = TipoDominio.objects.get(descripcion = 'Compartido').id
    comparte_otro_nivel_id = TipoCompartido.objects.get(descripcion = 'Establecimiento de otro nivel').id

    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_informacion_edilicia.html',
        'establecimiento': establecimiento,
        'es_dominio_compartido_id': es_dominio_compartido_id,
        'comparte_otro_nivel_id': comparte_otro_nivel_id,
        'page_title': 'Información edilicia',
        'actual_page': 'informacion_edilicia',
    })

@login_required
@credential_required('reg_establecimiento_completar')
def completar_conexion_internet(request):
    """
    CU 26
    """
    establecimiento = __get_establecimiento_actual(request)
    try:
        conexion = EstablecimientoConexionInternet.objects.get(establecimiento = establecimiento)
    except:
        conexion = EstablecimientoConexionInternet()
        conexion.establecimiento = establecimiento

    if request.method == 'POST':
        form = EstablecimientoConexionInternetForm(request.POST, instance = conexion)
        if form.is_valid():
            conexion = form.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoConexionInternetForm(instance = conexion)

    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_conexion_internet.html',
        'establecimiento': establecimiento,
        'page_title': 'Conexión a internet',
        'actual_page': 'conexion_internet',
    })

@login_required
@credential_required('reg_establecimiento_ver')
def datos_establecimiento(request):
    establecimiento = __get_establecimiento_actual(request)
    return my_render(request, 'registro/establecimiento/datos_establecimiento.html', {
        'establecimiento': establecimiento,
        'turnos': establecimiento.turnos.all(),
        'funciones': establecimiento.funciones.all(),
        'niveles': establecimiento.niveles.all(),
    })

@login_required
@credential_required('revisar_jurisdiccion')
def revisar_jurisdiccion(request, establecimiento_id):
    establecimiento = Establecimiento.objects.get(pk = establecimiento_id)
    establecimiento.revisado_jurisdiccion = True
    establecimiento.save()
    request.set_flash('success', 'Registro revisado.')
    return HttpResponseRedirect(reverse('establecimiento'))

