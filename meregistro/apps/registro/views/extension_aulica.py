# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.Localidad import Localidad
from apps.registro.models.EstadoExtensionAulica import EstadoExtensionAulica
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.ExtensionAulicaEstado import ExtensionAulicaEstado
from apps.registro.models.ExtensionAulicaDomicilio import ExtensionAulicaDomicilio
from apps.registro.models.ExtensionAulicaBaja import ExtensionAulicaBaja
from apps.registro.models.ExtensionAulicaInformacionEdilicia import ExtensionAulicaInformacionEdilicia
from apps.registro.models.ExtensionAulicaConexionInternet import ExtensionAulicaConexionInternet
from apps.registro.forms import ExtensionAulicaFormFilters, ExtensionAulicaForm, ExtensionAulicaDomicilioForm, ExtensionAulicaBajaForm, ExtensionAulicaContactoForm, ExtensionAulicaNivelesForm, ExtensionAulicaTurnosForm, ExtensionAulicaFuncionesForm, ExtensionAulicaInformacionEdiliciaForm, ExtensionAulicaConexionInternetForm, ExtensionAulicaCambiarEstadoForm
from helpers.MailHelper import MailHelper
from django.core.paginator import Paginator
import datetime
from apps.reportes.views.extension_aulica import extensiones_aulicas as reporte_extensiones_aulicas
from apps.reportes.models import Reporte
from apps.registro.models.TipoDominio import TipoDominio
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.FSM import FSMExtensionAulica

fsmExtensionAulica = FSMExtensionAulica()

ITEMS_PER_PAGE = 50

def __puede_verificar_datos(request):
    return request.has_credencial('reg_extension_aulica_verificar_datos')

def __pertenece_al_establecimiento(request, extension_aulica):
    """
    La extensión áulica pertenece al establecimiento?
    """
    return extension_aulica.ambito.path == request.get_perfil().ambito.path


def __extension_aulica_dentro_del_ambito(request, extension_aulica):
    """
    La extensión áulica está dentro del ámbito?
    """
    try:
        extension_aulica = ExtensionAulica.objects.get(id=extension_aulica.id, ambito__path__istartswith=request.get_perfil().ambito.path)
    except extension_aulica.DoesNotExist:
        return False
    return True

def __get_extension_aulica(request, extension_aulica_id):
    
    extension_aulica = ExtensionAulica.objects.get(pk=extension_aulica_id)

    if not __extension_aulica_dentro_del_ambito(request, extension_aulica):
        raise Exception('La extensión áulica no se encuentra en su ámbito.')

    return extension_aulica

@login_required
@credential_required('reg_extension_aulica_consulta')
def index(request):
    """
    Búsqueda de extensiones áulicas
    """
    if request.method == 'GET':
        form_filter = ExtensionAulicaFormFilters(request.GET)
    else:
        form_filter = ExtensionAulicaFormFilters()
    q = build_query(form_filter, 1, request)

    try:
        if request.GET['export'] == '1':
            return reporte_extensiones_aulicas(request, q)
    except KeyError:
        pass

    jurisdiccion = request.get_perfil().jurisdiccion()
    if jurisdiccion is not None:
        form_filter.fields["establecimiento"].queryset = Establecimiento.objects.filter(dependencia_funcional__jurisdiccion__id=jurisdiccion.id)
    form_filter.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith=request.get_perfil().ambito.path)
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
    return my_render(request, 'registro/extension_aulica/index.html', {
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


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('nombre').filter(establecimiento__ambito__path__istartswith=request.get_perfil().ambito.path)


@login_required
@credential_required('reg_extension_aulica_alta')
def create(request):
    """
    Alta de extensión áulica.
    """
    if request.method == 'POST':
        form = ExtensionAulicaForm(request.POST)
        if form.is_valid():
            ext = form.save(commit=False)
            estado = EstadoExtensionAulica.objects.get(nombre=EstadoExtensionAulica.PENDIENTE)
            ext.estado = estado
            ext.fecha_alta = datetime.date.today()
            ext.save()
            ext.registrar_estado()

            MailHelper.notify_by_email(MailHelper.EXTENSION_AULICA_CREATE, ext)
            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('extensionAulica'))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = ExtensionAulicaForm()
        
    jurisdiccion = request.get_perfil().jurisdiccion()
    form.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith=request.get_perfil().ambito.path)

    return my_render(request, 'registro/extension_aulica/new.html', {
        'form': form,
        'is_new': True,
    })


@login_required
@credential_required('reg_extension_aulica_baja')
def delete(request, extension_aulica_id):
    ext = ExtensionAulica.objects.get(pk=extension_aulica_id)
    if not __extension_aulica_dentro_del_ambito(request, ext):
        raise Exception('La unidad educativa no está en el ámbito del usuario.')
    elif not ext.is_deletable():
       request.set_flash('warning', 'La unidad educativa no se puede eliminar.')
    else:
        ext.delete()
        request.set_flash('success', 'Registro eliminado correctamente.')
    return HttpResponseRedirect(reverse('extensionAulica'))


@login_required
@credential_required('reg_extension_aulica_baja')
def baja(request, extension_aulica_id):
    """
    Baja de un extensión áulica
    CU 28
    """
    extension_aulica = ExtensionAulica.objects.get(pk=extension_aulica_id)
    """ Pertenece al establecimiento? """
    pertenece_al_establecimiento = __pertenece_al_establecimiento(request, extension_aulica)
    if not pertenece_al_establecimiento:
        raise Exception('La extensión áulica no pertenece al establecimiento.')
    """ La extensión áulica ya fue dada de baja? """
    dada_de_baja = extension_aulica.dadaDeBaja()
    if dada_de_baja:
        request.set_flash('notice', 'La extensión áulica ya se encuentra dada de baja.')
    """ Continuar """
    if request.method == 'POST':
        form = ExtensionAulicaBajaForm(request.POST)
        if form.is_valid():
            baja = form.save(commit=False)
            baja.extension_aulica = extension_aulica
            baja.save()
            estado = EstadoExtensionAulica.objects.get(nombre=EstadoExtensionAulica.BAJA)
            extension_aulica.estado = estado
            extension_aulica.save()
            extension_aulica.registrar_estado()

            dado_de_baja = True

            request.set_flash('success', 'La extensión áulica fue dada de baja correctamente.')
            """ Redirecciono para evitar el reenvío del form """
            return HttpResponseRedirect(reverse('extensionAulica'))
        else:
            request.set_flash('warning', 'Ocurrió un error dando de baja la extensión áulica.')
    else:
        form = ExtensionAulicaBajaForm()
    return my_render(request, 'registro/extension_aulica/baja.html', {
        'form': form,
        'extension_aulica': extension_aulica,
        'dada_de_baja': dada_de_baja,
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def completar_datos(request):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'establecimiento': establecimiento,
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def completar_datos_basicos(request, extension_aulica_id):
    """
    Edición de los datos de una extensión áulica.
    """
    ext = __get_extension_aulica(request, extension_aulica_id)
    if request.method == 'POST':
        form = ExtensionAulicaForm(request.POST, instance=ext)
        if form.is_valid():
            ext = form.save()
            if __puede_verificar_datos(request):
                v = ext.get_verificacion_datos()
                v.datos_basicos = form.cleaned_data['verificado']
                v.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            raise Exception(form.errors)
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = ExtensionAulicaForm(instance=ext)

    jurisdiccion = request.get_perfil().jurisdiccion()
    form.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith=request.get_perfil().ambito.path)
    try:
        codigo = Establecimiento.get_parts_from_cue(ext.cue)['codigo_tipo_unidad_educativa']
    except TypeError:
        codigo = ''
    form.initial['verificado'] = ext.get_verificacion_datos().datos_basicos
    return my_render(request, 'registro/extension_aulica/completar_datos.html', {
        'form': form,
        'form_template': 'registro/extension_aulica/form_datos_basicos.html',
        'extension_aulica': ext,
        'codigo_tipo_unidad_educativa': codigo,
        'page_title': 'Datos básicos',
        'actual_page': 'datos_basicos'
    })    


@login_required
@credential_required('reg_extension_aulica_modificar')
def completar_contacto(request, extension_aulica_id):
    ext = ExtensionAulica.objects.get(pk=extension_aulica_id)

    if not __extension_aulica_dentro_del_ambito(request, ext):
        raise Exception('La extensión áulica no se encuentra en su ámbito.')

    if request.method == 'POST':
        form = ExtensionAulicaContactoForm(request.POST, instance=ext)
        if form.is_valid():
            ext = form.save()
            if __puede_verificar_datos(request):
                v = ext.get_verificacion_datos()
                v.contacto = form.cleaned_data['verificado']
                v.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = ExtensionAulicaContactoForm(instance=ext)
    form.initial['verificado'] = ext.get_verificacion_datos().contacto
    return my_render(request, 'registro/extension_aulica/completar_datos.html', {
        'form': form,
        'form_template': 'registro/extension_aulica/form_contacto.html',
        'extension_aulica': ext,
        'page_title': 'Contacto',
        'actual_page': 'contacto',
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def completar_niveles(request, extension_aulica_id):
    """
    CU 26
    """
    ext = __get_extension_aulica(request, extension_aulica_id)

    if request.method == 'POST':
        form = ExtensionAulicaNivelesForm(request.POST, instance=ext)
        if form.is_valid():
            niveles = form.save()
            if __puede_verificar_datos(request):
                v = ext.get_verificacion_datos()
                v.niveles = form.cleaned_data['verificado']
                v.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = ExtensionAulicaNivelesForm(instance=ext)
    form.initial['verificado'] = ext.get_verificacion_datos().niveles
    return my_render(request, 'registro/extension_aulica/completar_datos.html', {
        'form': form,
        'form_template': 'registro/extension_aulica/form_niveles.html',
        'extension_aulica': ext,
        'page_title': 'Niveles',
        'actual_page': 'niveles',
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def completar_turnos(request, extension_aulica_id):
    ext = __get_extension_aulica(request, extension_aulica_id)

    if request.method == 'POST':
        form = ExtensionAulicaTurnosForm(request.POST, instance=ext)
        if form.is_valid():
            turnos = form.save()
            if __puede_verificar_datos(request):
                v = ext.get_verificacion_datos()
                v.turnos = form.cleaned_data['verificado']
                v.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = ExtensionAulicaTurnosForm(instance=ext)
    form.initial['verificado'] = ext.get_verificacion_datos().turnos
    return my_render(request, 'registro/extension_aulica/completar_datos.html', {
        'form': form,
        'form_template': 'registro/extension_aulica/form_turnos.html',
        'extension_aulica': ext,
        'page_title': 'Turnos',
        'actual_page': 'turnos',
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def completar_funciones(request, extension_aulica_id):
    ext = __get_extension_aulica(request, extension_aulica_id)

    if request.method == 'POST':
        form = ExtensionAulicaFuncionesForm(request.POST, instance=ext)
        if form.is_valid():
            funciones = form.save()
            if __puede_verificar_datos(request):
                v = ext.get_verificacion_datos()
                v.funciones = form.cleaned_data['verificado']
                v.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = ExtensionAulicaFuncionesForm(instance=ext)
    form.initial['verificado'] = ext.get_verificacion_datos().funciones
    return my_render(request, 'registro/extension_aulica/completar_datos.html', {
        'form': form,
        'form_template': 'registro/extension_aulica/form_funciones.html',
        'extension_aulica': ext,
        'page_title': 'Funciones',
        'actual_page': 'funciones',
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def completar_informacion_edilicia(request, extension_aulica_id):
    """
    CU 26
    """
    extension_aulica = __get_extension_aulica(request, extension_aulica_id)
    try:
        informacion_edilicia = ExtensionAulicaInformacionEdilicia.objects.get(extension_aulica=extension_aulica)
    except:
        informacion_edilicia = ExtensionAulicaInformacionEdilicia()
        informacion_edilicia.extension_aulica = extension_aulica

    if request.method == 'POST':
        form = ExtensionAulicaInformacionEdiliciaForm(request.POST, instance=informacion_edilicia)
        if form.is_valid():
            informacion_edilicia = form.save()
            if __puede_verificar_datos(request):
                v = extension_aulica.get_verificacion_datos()
                v.info_edilicia = form.cleaned_data['verificado']
                v.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = ExtensionAulicaInformacionEdiliciaForm(instance=informacion_edilicia)

    es_dominio_compartido_id = TipoDominio.objects.get(descripcion='Compartido').id
    comparte_otro_nivel_id = TipoCompartido.objects.get(descripcion='Establecimiento de otro nivel').id
    form.initial['verificado'] = extension_aulica.get_verificacion_datos().info_edilicia
    return my_render(request, 'registro/extension_aulica/completar_datos.html', {
        'form': form,
        'form_template': 'registro/extension_aulica/form_informacion_edilicia.html',
        'extension_aulica': extension_aulica,
        'es_dominio_compartido_id': es_dominio_compartido_id,
        'comparte_otro_nivel_id': comparte_otro_nivel_id,
        'page_title': 'Información edilicia',
        'actual_page': 'informacion_edilicia',
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def completar_conexion_internet(request, extension_aulica_id):
    """
    CU 26
    """
    extension_aulica = __get_extension_aulica(request, extension_aulica_id)
    try:
        conexion = ExtensionAulicaConexionInternet.objects.get(extension_aulica=extension_aulica)
    except:
        conexion = ExtensionAulicaConexionInternet()
        conexion.extension_aulica = extension_aulica

    if request.method == 'POST':
        form = ExtensionAulicaConexionInternetForm(request.POST, instance=conexion)
        if form.is_valid():
            conexion = form.save()
            if __puede_verificar_datos(request):
                v = extension_aulica.get_verificacion_datos()
                v.conectividad = form.cleaned_data['verificado']
                v.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = ExtensionAulicaConexionInternetForm(instance=conexion)
    form.initial['verificado'] = extension_aulica.get_verificacion_datos().conectividad
    return my_render(request, 'registro/extension_aulica/completar_datos.html', {
        'form': form,
        'form_template': 'registro/extension_aulica/form_conexion_internet.html',
        'extension_aulica': extension_aulica,
        'page_title': 'Conexión a internet',
        'actual_page': 'conexion_internet',
    })


@login_required
@credential_required('reg_anexo_aprobar_registro')
def registrar(request, extension_aulica_id):
    extension_aulica = ExtensionAulica.objects.get(pk=extension_aulica_id)
    form = __registrar_get_form(request, extension_aulica)
    if request.method == 'POST' and __registrar_process(request, form, extension_aulica):
            return HttpResponseRedirect(reverse('extensionAulica'))
    return __registrar_show_form(request, form, extension_aulica)


def __registrar_get_form(request, extension_aulica):
    if request.method == 'POST':
        form = ExtensionAulicaCambiarEstadoForm(request.POST)
    else:
        form = ExtensionAulicaCambiarEstadoForm()
    form.fields["estado"].choices = map(lambda e: (e.id, e), fsmExtensionAulica.estadosDesde(extension_aulica.estado_actual))
    return form


def __registrar_show_form(request, form, extension_aulica):
    return my_render(request, 'registro/extension_aulica/registrar.html', {
        'form': form,
        'extension_aulica': extension_aulica
    })


def __registrar_process(request, form, extension_aulica):
    if form.is_valid():
        nuevoEstado = form.cleaned_data['estado']
        try:
            extension_aulica.estado = nuevoEstado
            extension_aulica.save()
            extension_aulica.registrar_estado()
            request.set_flash('success', 'Extensión Áulica registrada correctamente.')
            return True
        except:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    return False

@credential_required('reg_extension_aulica_verificar_datos')
def verificar_dato(request, extension_aulica_id):
    extension_aulica = ExtensionAulica.objects.get(pk=extension_aulica_id)
    verificacion = extension_aulica.get_verificacion_datos()
    value = request.GET['verificado'] == 'true'
    if request.GET['dato'] == 'domicilios':
        verificacion.domicilios = value
    elif request.GET['dato'] == 'autoridades':
        verificacion.autoridades = value
    verificacion.save()
    return HttpResponse('ok')
