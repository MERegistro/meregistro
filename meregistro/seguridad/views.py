# -*- coding: UTF-8 -*-

from meregistro.shortcuts import my_render
from forms import LoginForm
from authenticate import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

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
        return HttpResponseRedirect(reverse('seleccionarPerfil'))
  else:
    form = LoginForm()
  return my_render(request, 'login/login.html', {'form': form})
  
def seleccionarPerfil(request):
  return HttpResponse('hola ' + str(request.user.is_anonymous()))
