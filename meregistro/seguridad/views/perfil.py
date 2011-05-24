# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from seguridad.decorators import login_required
from seguridad.models import Usuario
from seguridad.forms import AsignarPerfilForm


@login_required
def verPerfilesUsuario(request, userId):
  usuario = Usuario.objects.get(pk=userId)
  return my_render(request, 'seguridad/perfil/verPerfilesUsuario.html', {
    'usuario': usuario
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

  return my_render(request, 'seguridad/perfil/new.html', {
    'form': form,
    'usuario': usuario,
  })
