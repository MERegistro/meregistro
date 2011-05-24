# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from seguridad.decorators import login_required
from seguridad.models import Usuario, Perfil, MotivoBloqueo
from seguridad.forms import UsuarioFormFilters, UsuarioForm, UsuarioCreateForm
from seguridad.forms import UsuarioChangePasswordForm, BloquearUsuarioForm, DesbloquearUsuarioForm


@login_required
def index(request):
  """
  Búsqueda de usuarios
  """
  if request.method == 'POST':
    form_filter = UsuarioFormFilters(request.POST)
  else:
    form_filter = UsuarioFormFilters()
  q = build_query(form_filter, 1)
  return my_render(request, 'seguridad/usuario/index.html', {
    'form_filters': form_filter,
    'objects': q
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

  return my_render(request, 'seguridad/usuario/new.html', {
    'form': form,
  })


@login_required
def change_password(request, userId):
  """
  Cambiar contraseña de un usuario.
  """
  usuario = Usuario.objects.get(pk=userId)
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
    'form': form
  })


@login_required
def desbloquear(request, userId):
  """
  Desbloquea un usuario.
  """
  usuario = Usuario.objects.get(pk=userId)
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
    'form': form
  })
