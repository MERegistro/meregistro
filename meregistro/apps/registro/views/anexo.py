# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.Anexo import Anexo
from apps.registro.models.Localidad import Localidad
from apps.registro.models.EstadoAnexo import EstadoAnexo
from apps.registro.models.AnexoEstado import AnexoEstado
from apps.registro.models.AnexoDomicilio import AnexoDomicilio
from apps.registro.models.AnexoInformacionEdilicia import AnexoInformacionEdilicia
from apps.registro.models.AnexoConexionInternet import AnexoConexionInternet
from apps.registro.models.TipoDominio import TipoDominio
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.forms import AnexoFormFilters, AnexoForm, AnexoDomicilioForm, AnexoBajaForm, AnexoDatosBasicosForm, AnexoTurnosForm, AnexoDomicilioForm
from apps.registro.forms.AnexoNivelesForm import AnexoNivelesForm
from apps.registro.forms.AnexoFuncionesForm import AnexoFuncionesForm
from apps.registro.forms.AnexoInformacionEdiliciaForm import AnexoInformacionEdiliciaForm
from apps.registro.forms.AnexoConexionInternetForm import AnexoConexionInternetForm
from helpers.MailHelper import MailHelper
from django.core.paginator import Paginator
import datetime

ITEMS_PER_PAGE = 50

"""
El anexo pertenece al establecimiento?
"""
def __pertenece_al_establecimiento(request, anexo):
    return anexo.establecimiento.ambito.path == request.get_perfil().ambito.path

@login_required
@credential_required('reg_anexo_consulta')
def index(request):
    """
    Búsqueda de anexos
    """
    if request.method == 'GET':
        form_filter = AnexoFormFilters(request.GET)
    else:
        form_filter = AnexoFormFilters()
    q = build_query(form_filter, 1, request)

    jurisdiccion = request.get_perfil().jurisdiccion()
    if jurisdiccion is not None:
        form_filter.fields["establecimiento"].queryset = Establecimiento.objects.filter(dependencia_funcional__jurisdiccion__id = jurisdiccion.id)
    form_filter.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith = request.get_perfil().ambito.path)
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
    return my_render(request, 'registro/anexo/index.html', {
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
    return filters.buildQuery().order_by('establecimiento__nombre', 'cue').filter(ambito__path__istartswith = request.get_perfil().ambito.path)


@login_required
@credential_required('reg_anexo_alta')
def create(request):
    """
    Alta de anexo.
    """
    if request.method == 'POST':
        form = AnexoForm(request.POST)
        domicilio_form = AnexoDomicilioForm(request.POST)
        if form.is_valid() and domicilio_form.is_valid():

            anexo = form.save(commit = False)
            estado = EstadoAnexo.objects.get(nombre = EstadoAnexo.VIGENTE)
            anexo.estado = estado
            anexo.save()
            anexo.registrar_estado()

            domicilio = domicilio_form.save(commit = False)
            domicilio.anexo = anexo
            domicilio.save()

            form.save_m2m() # Guardo las relaciones - https://docs.djangoproject.com/en/1.2/topics/forms/modelforms/#the-save-method
            
            MailHelper.notify_by_email(MailHelper.ANEXO_CREATE, anexo)
            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('anexoEdit', args=[anexo.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = AnexoForm()
        domicilio_form = AnexoDomicilioForm()

    jurisdiccion = request.get_perfil().jurisdiccion()
    form.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith = request.get_perfil().ambito.path)
    if jurisdiccion is not None:
        domicilio_form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id = jurisdiccion.id)

    return my_render(request, 'registro/anexo/new.html', {
        'form': form,
        'domicilio_form': domicilio_form,
        'is_new': True,
    })


@login_required
@credential_required('reg_anexo_modificar')
def edit(request, anexo_id):
    """
    Edición de los datos de un anexo.
    """
    anexo = Anexo.objects.get(pk = anexo_id)
    if anexo.dadoDeBaja():
        raise Exception('El anexo se encuentra dado de baja.')
    if not __pertenece_al_establecimiento(request, anexo):
        raise Exception('El anexo no pertenece a su establecimiento.')
    try:
        domicilio = AnexoDomicilio.objects.get(anexo = anexo)
    except:
        domicilio = AnexoDomicilio()
        domicilio.anexo = anexo
    if request.method == 'POST':
        form = AnexoForm(request.POST, instance = anexo)
        domicilio_form = AnexoDomicilioForm(request.POST, instance = domicilio)
        if form.is_valid() and domicilio_form.is_valid():
            anexo = form.save()
            domicilio = domicilio_form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoForm(instance = anexo)
        domicilio_form = AnexoDomicilioForm(instance = domicilio)

    jurisdiccion = request.get_perfil().jurisdiccion()
    form.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith = request.get_perfil().ambito.path)
    if jurisdiccion is not None:
        domicilio_form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id = jurisdiccion.id)
    return my_render(request, 'registro/anexo/edit.html', {
        'form': form,
        'domicilio_form': domicilio_form,
        'domicilio': domicilio,
        'anexo': anexo,
    })

@login_required
@credential_required('reg_anexo_baja')
def baja(request, anexo_id):
    """
    Baja de un anexo
    CU 28
    """
    anexo = Anexo.objects.get(pk = anexo_id)
    """ Pertenece al establecimiento? """
    pertenece_al_establecimiento = __pertenece_al_establecimiento(request, anexo)
    if not pertenece_al_establecimiento:
        raise Exception('El anexo no pertenece a su establecimiento.')
    """ El anexo ya fue dado de baja? """
    dado_de_baja = anexo.dadoDeBaja()
    if dado_de_baja:
        request.set_flash('notice', 'El anexo ya se encuentra dado de baja.')
    """ Continuar """
    if request.method == 'POST':
        form = AnexoBajaForm(request.POST)
        if form.is_valid():
            baja = form.save(commit = False)
            baja.anexo = anexo
            baja.save()
            estado = EstadoAnexo.objects.get(nombre = EstadoAnexo.BAJA)
            anexo.estado = estado
            anexo.save()
            anexo.registrar_estado()
            dado_de_baja = True

            request.set_flash('success', 'El anexo fue dado de baja correctamente.')
            """ Redirecciono para evitar el reenvío del form """
            return HttpResponseRedirect(reverse('anexo'))
        else:
            request.set_flash('warning', 'Ocurrió un error dando de baja el anexo.')
    else:
        form = AnexoBajaForm()
    return my_render(request, 'registro/anexo/baja.html', {
        'form': form,
        'anexo': anexo,
        'dado_de_baja': dado_de_baja,
    })

def __get_anexo_actual(request):
    """
    Trae el único anexo que tiene asignado el usuario
    """
    anexos = Anexo.objects.filter(ambito__path__istartswith = request.get_perfil().ambito.path)
    if len(anexos) == 0:
        raise Exception('ERROR: El usuario no tiene asignado un anexo.')
    elif len(anexos) == 1:
        return anexos[0]
    else:
        pass

@login_required
#@credential_required('reg_establecimiento_completar')
def completar_datos_basicos(request):
    anexo = __get_anexo_actual(request)
    if request.method == 'POST':
        form = AnexoDatosBasicosForm(request.POST, instance = anexo)
        if form.is_valid():
            anexo = form.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoDatosBasicosForm(instance = anexo)

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_datos_basicos.html',
        'anexo': anexo,
        'page_title': 'Datos básicos',
        'actual_page': 'datos_basicos',
    })

@login_required
#@credential_required('reg_establecimiento_completar')
def completar_turnos(request):
    """
    CU 26
    """
    anexo = __get_anexo_actual(request)

    if request.method == 'POST':
        form = AnexoTurnosForm(request.POST, instance = anexo)
        if form.is_valid():
            turnos = form.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoTurnosForm(instance = anexo)

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_turnos.html',
        'anexo': anexo,
        'page_title': 'Turnos',
        'actual_page': 'turnos',
    })

@login_required
#@credential_required('reg_establecimiento_completar')
def completar_domicilio(request):
    """
    CU 26
    """
    anexo = __get_anexo_actual(request)
    try:
        domicilio = anexo.anexo_domicilio.get()
    except:
        domicilio = AnexoDomicilio()
        domicilio.anexo = anexo

    if request.method == 'POST':
        form = AnexoDomicilioForm(request.POST, instance = domicilio)
        if form.is_valid():
            domicilio = form.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoDomicilioForm(instance = domicilio)

    jurisdiccion = request.get_perfil().jurisdiccion()
    form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id = jurisdiccion.id)

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_domicilio.html',
        'anexo': anexo,
        'page_title': 'Domicilio',
        'actual_page': 'domicilio',
    })

@login_required
#@credential_required('reg_establecimiento_completar')
def completar_niveles(request):
    """
    CU 26
    """
    anexo = __get_anexo_actual(request)

    if request.method == 'POST':
        form = AnexoNivelesForm(request.POST, instance = anexo)
        if form.is_valid():
            niveles = form.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoNivelesForm(instance = anexo)

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_niveles.html',
        'anexo': anexo,
        'page_title': 'Niveles',
        'actual_page': 'niveles',
    })

@login_required
#@credential_required('reg_establecimiento_completar')
def completar_funciones(request):
    """
    CU 26
    """
    anexo = __get_anexo_actual(request)

    if request.method == 'POST':
        form = AnexoFuncionesForm(request.POST, instance = anexo)
        if form.is_valid():
            funciones = form.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoFuncionesForm(instance = anexo)

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_funciones.html',
        'anexo': anexo,
        'page_title': 'Funciones',
        'actual_page': 'funciones',
    })


@login_required
#@credential_required('reg_establecimiento_completar')
def completar_informacion_edilicia(request):
    """
    CU 26
    """
    anexo = __get_anexo_actual(request)

    try:
        informacion_edilicia = AnexoInformacionEdilicia.objects.get(anexo = anexo)
    except:
        informacion_edilicia = AnexoInformacionEdilicia()
        informacion_edilicia.anexo = anexo

    if request.method == 'POST':
        form = AnexoInformacionEdiliciaForm(request.POST, instance = informacion_edilicia)
        if form.is_valid():
            informacion_edilicia = form.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, anexo)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoInformacionEdiliciaForm(instance = informacion_edilicia)

    es_dominio_compartido_id = TipoDominio.objects.get(descripcion = 'Compartido').id
    comparte_otro_nivel_id = TipoCompartido.objects.get(descripcion = 'Establecimiento de otro nivel').id

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_informacion_edilicia.html',
        'anexo': anexo,
        'es_dominio_compartido_id': es_dominio_compartido_id,
        'comparte_otro_nivel_id': comparte_otro_nivel_id,
        'page_title': 'Información edilicia',
        'actual_page': 'informacion_edilicia',
    })

@login_required
#@credential_required('reg_anexo_completar')
def completar_conexion_internet(request):
    """
    CU 26
    """
    anexo = __get_anexo_actual(request)
    try:
        conexion = AnexoConexionInternet.objects.get(anexo = anexo)
    except:
        conexion = AnexoConexionInternet()
        conexion.anexo = anexo

    if request.method == 'POST':
        form = AnexoConexionInternetForm(request.POST, instance = conexion)
        if form.is_valid():
            conexion = form.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, anexo)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoConexionInternetForm(instance = conexion)

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_conexion_internet.html',
        'anexo': anexo,
        'page_title': 'Conexión a internet',
        'actual_page': 'conexion_internet',
    })


