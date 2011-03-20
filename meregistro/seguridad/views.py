# -*- coding: UTF-8 -*-

from meregistro.shortcuts import my_render
from forms import LoginForm, SeleccionarPerfilForm
from authenticate import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from decorators import login_required

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
  return my_render(request, 'login/login.html', {'form': form})

@login_required
def seleccionarPerfil(request):
  if request.method == 'POST':
    form = SeleccionarPerfilForm(request.user, request.POST)
    if form.is_valid():
      request.seleccionar_perfil(form.cleaned_data['perfil'])
      return HttpResponseRedirect(reverse('seguridadHome'))
  else:
    form = SeleccionarPerfilForm(request.user)
  return my_render(request, 'seleccionarPerfil/seleccionarPerfil.html', {'form': form})

def index(request):
  return HttpResponse('hola' + request.get_perfil().rol.nombre)
