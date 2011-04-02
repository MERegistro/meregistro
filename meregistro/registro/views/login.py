# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from seguridad.forms import LoginForm, SeleccionarPerfilForm
from seguridad.authenticate import authenticate
from seguridad.decorators import login_required

def login(request):
  """
  Pantalla de login al sistema.
  Si el request.method es POST, valida que la contraseña sea correcta y
  en tal caso redirige a seleccionarPerfil.
  """
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      user = authenticate(
        form.cleaned_data['tipo_documento'],
        form.cleaned_data['documento'],
        form.cleaned_data['password'],
      )
      if user:
        request.session['user_id'] = user.id
        # Se logueo bien, lo redirijo a seleccionarPerfil
        return HttpResponseRedirect(reverse('seleccionarPerfil'))
  else:
    form = LoginForm()
  return my_render(request, 'seguridad/login/login.html', {'form': form})

@login_required
def seleccionar_perfil(request):
  if request.method == 'POST':
    form = SeleccionarPerfilForm(request.user, request.POST)
    if form.is_valid():
      request.seleccionar_perfil(form.cleaned_data['perfil'])
      return HttpResponseRedirect(reverse('home'))
  else:
    form = SeleccionarPerfilForm(request.user)
  return my_render(request, 'seguridad/login/seleccionarPerfil.html', {'form': form})
