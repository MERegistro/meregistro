# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required
from apps.seguridad.models import Usuario, Perfil, MotivoBloqueo, Rol
from apps.seguridad.forms import UsuarioFormFilters, UsuarioForm, UsuarioCreateForm, UsuarioPasswordForm
from apps.seguridad.forms import UsuarioChangePasswordForm, BloquearUsuarioForm, DesbloquearUsuarioForm, UsuarioEditarDatosForm
from django.core.paginator import Paginator
from apps.reportes.views.usuario import usuarios as reporte_usuarios
from apps.reportes.models import Reporte

ITEMS_PER_PAGE = 50

def __check_puede_modificar_usuario(request, usuario):
    if not request.get_perfil().can_modificar_usuario(usuario): 
        raise Exception('No puede modificar al usuario')

@login_required
def index(request):
    """
    Búsqueda de usuarios
    """
    if request.method == 'GET':
        form_filter = UsuarioFormFilters(request.GET)
    else:
        form_filter = UsuarioFormFilters()
    q = build_query(form_filter, 1)
    q.filter(perfiles__ambito__path__istartswith=request.get_perfil().ambito.path)

    try:
        if request.GET['export'] == '1':
            return reporte_usuarios(request, q)
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
    return my_render(request, 'seguridad/usuario/index.html', {
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'export_url': Reporte.build_export_url(request.build_absolute_uri()),
        'usuario_activo_id': request.get_perfil().usuario.id,
    })


def build_query(filters, page):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('apellido', 'nombre')


@login_required
def edit(request, userId):
    """
    Edición de los datos de un usuario.
    """
    usuario = Usuario.objects.get(pk=userId)
    if request.method == 'POST':
        __check_puede_modificar_usuario(request, usuario)
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = UsuarioForm(instance=usuario)
    return my_render(request, 'seguridad/usuario/edit.html', {
        'form': form,
        'usuario': usuario,
        'modificable': request.get_perfil().can_modificar_usuario(usuario)
    })


@login_required
def create(request):
    """
    Alta de usuario.
    """
    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.is_active = True
            usuario.save()
            perfil = Perfil()
            perfil.usuario = usuario
            perfil.rol = form.cleaned_data['rol']
            perfil.ambito = form.cleaned_data['ambito']
            perfil.fecha_asignacion = datetime.now()
            perfil.save()
            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('usuarioEdit', args=[usuario.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = UsuarioCreateForm()
    form.fields['rol'].queryset = request.get_perfil().rol.roles_asignables.all()

    return my_render(request, 'seguridad/usuario/new.html', {
        'form': form,
    })


@login_required
def change_password(request, userId):
    """
    Cambiar contraseña de un usuario.
    """
    usuario = Usuario.objects.get(pk=userId)
    __check_puede_modificar_usuario(request, usuario)
    if request.method == 'POST':
        form = UsuarioChangePasswordForm(request.POST)
        if form.is_valid():
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            request.set_flash('success', 'Contraseña modificada correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error modificando la contraseña.')
    else:
        form = UsuarioChangePasswordForm()

    return my_render(request, 'seguridad/usuario/change_password.html', {
        'form': form,
        'usuario': usuario,
    })


@login_required
def bloquear(request, userId):
    """
    Bloquea un usuario.
    """
    usuario = Usuario.objects.get(pk=userId)
    __check_puede_modificar_usuario(request, usuario)
    if not request.get_perfil().ve_usuario(usuario):
        request.set_flash('warning', 'No puede bloquear el usuario seleccionado.')
        return HttpResponseRedirect(reverse('usuarioEdit', args=[userId]))
    if request.method == 'POST':
        form = BloquearUsuarioForm(request.POST)
        if form.is_valid():
            usuario.lock(form.cleaned_data['motivo'])
            request.set_flash('success', 'Usuario bloqueado correctamente')
            return HttpResponseRedirect(reverse('usuarioEdit', args=[userId]))
        else:
            request.set_flash('warning', 'Ocurrió un error bloqueando al usuario.')
    else:
        form = BloquearUsuarioForm()
    return my_render(request, 'seguridad/usuario/bloquear.html', {
        'usuario': usuario,
        'form': form})


@login_required
def desbloquear(request, userId):
    """
    Desbloquea un usuario.
    """
    usuario = Usuario.objects.get(pk=userId)
    __check_puede_modificar_usuario(request, usuario)
    if request.method == 'POST':
        form = DesbloquearUsuarioForm(request.POST)
        if form.is_valid():
            usuario.unlock(form.cleaned_data['motivo'])
            request.set_flash('success', 'Usuario desbloqueado correctamente')
            return HttpResponseRedirect(reverse('usuarioEdit', args=[userId]))
        else:
            request.set_flash('warning', 'Ocurrió un error desbloqueando al usuario.')
    else:
        form = DesbloquearUsuarioForm()
    return my_render(request, 'seguridad/usuario/desbloquear.html', {
        'usuario': usuario,
        'form': form})


@login_required
def editarDatosPropios(request):
    if request.method == 'POST':
        form = UsuarioEditarDatosForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            request.user.nombre = usuario.nombre
            request.user.apellido = usuario.apellido
            request.user.email = usuario.email
            request.user.save()
            request.set_flash('success', 'Datos guardados correctamente')
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos')
    else:
        form = UsuarioEditarDatosForm(instance=request.user)
    return my_render(request, 'seguridad/usuario/editarDatosPropios.html', {
        'form': form})


@login_required
def editarPasswordPropia(request):
    if request.method == 'POST':
        form = UsuarioPasswordForm(request.POST)
        from apps.seguridad.authenticate import encrypt_password
        if form.is_valid():
            if request.user.password == encrypt_password(form.cleaned_data['password_actual']):
                request.user.set_password(form.cleaned_data['password'])
                request.user.save()
                request.set_flash('success', 'Datos guardados correctamente')
            else:
                request.set_flash('warning', 'La contraseña actual no es correcta')
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos')
    else:
        form = UsuarioPasswordForm()
    return my_render(request, 'seguridad/usuario/editarPasswordPropia.html', {
        'form': form})


# Falta designar credenciales
@login_required
def delete(request, usuario_id):
    usuario_actual = request.get_perfil().usuario
    usuario_a_aliminar = Usuario.objects.get(pk=usuario_id)
    __check_puede_modificar_usuario(request, usuario_a_aliminar)
    if usuario_actual == usuario_a_aliminar:
        request.set_flash('warning', 'El usuario no puede eliminarse a sí mismo.')
    elif usuario_a_aliminar.is_deletable() and usuario_actual.can_delete_usuario(usuario_a_aliminar):
        usuario_a_aliminar.delete()
        request.set_flash('success', 'Usuario eliminado correctamente.')
    else: 
        request.set_flash('warning', 'El usuario no se puede eliminar.')
    return HttpResponseRedirect(reverse('usuario'))
