# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime, date
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required
from apps.seguridad.models import Usuario, Perfil
from apps.seguridad.forms import AsignarPerfilForm


@login_required
def verPerfilesUsuario(request, userId):
  usuario = Usuario.objects.get(pk=userId)
  perfiles = Perfil.objects.filter(usuario=usuario).order_by('-fecha_desasignacion', 'id')
  return my_render(request, 'seguridad/perfil/verPerfilesUsuario.html', {
    'usuario': usuario,
    'perfiles': perfiles,
    'perfil_activo_id': request.get_perfil().id,
  })


@login_required
def create(request, userId=None):
  """
  Asignacion de perfil a usuario.
  """
  usuario = Usuario.objects.get(pk=userId)
  if request.method == 'POST':
    form = AsignarPerfilForm(request.POST)
    if form.is_valid():
      usuario.asignarPerfil(form.cleaned_data['rol'], form.cleaned_data['ambito'], datetime.now())
      request.set_flash('success', 'Perfil asignado correctamente.')
      return HttpResponseRedirect(reverse('verPerfilesUsuario', args=[usuario.id]))
    else:
      request.set_flash('warning', 'Ocurrió un error asignando el perfil.')
  else:
    form = AsignarPerfilForm()
  form.fields["rol"].queryset = request.get_perfil().rol.roles_asignables
  return my_render(request, 'seguridad/perfil/new.html', {
    'form': form,
    'usuario': usuario,
  })

# Falta designar credenciales
@login_required
def delete(request, perfil_id):
    usuario_actual = request.get_perfil().usuario
    perfil = Perfil.objects.get(pk=perfil_id)  # Falta filtrar el usuario
    if perfil.is_deletable() and usuario_actual.can_delete_perfil(perfil):
        perfil.fecha_desasignacion = date.today()
        perfil.save()
        request.set_flash('success', 'Perfil eliminado correctamente.')
    else: 
        request.set_flash('error', 'El perfil no se puede eliminar.')
    return HttpResponseRedirect(reverse('verPerfilesUsuario', args=[perfil.usuario.id]))
