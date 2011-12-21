# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.forms import LoginForm, SeleccionarPerfilForm, RememberPasswordForm
from apps.seguridad.authenticate import authenticate
from apps.seguridad.decorators import login_required
from apps.seguridad.models import TipoDocumento, Usuario, PasswordRememberKey
from hashlib import sha1
import random
from helpers.MailHelper import MailHelper


def logout(request):
    """
    Logout y redireccionar a login.
    """
    request.logout()
    return HttpResponseRedirect(reverse('login'))


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
        form.cleaned_data['password'].strip(),
      )
      if user:
        if user.is_active:
          request.session['user_id'] = user.id
          # Se logueo bien, lo redirijo a seleccionarPerfil
          return HttpResponseRedirect(reverse('seleccionarPerfil'))
        else:
          request.set_flash('warning', 'No puede iniciar sesión: usuario bloqueado')
  else:
    init={}
    try:
        init['tipo_documento'] = TipoDocumento.objects.get(abreviatura='DNI').id
    except:
        pass
    form = LoginForm(initial=init)
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

def remember_password(request):
  if request.method == 'POST':
    form = RememberPasswordForm(request.POST)
    if form.is_valid():
      request.set_flash('success', 'Se el ha enviado un mail con instrucciones para resetear su contraseña.')
      user = Usuario.objects.filter(documento=form.cleaned_data['documento']).filter(tipo_documento=form.cleaned_data['tipo_documento']).all()[0]
      key = PasswordRememberKey()
      key.usuario = user
      tmp = ''.join(random.sample("1234567890qwertyuiopasdfghjklzxcvbnm", 32))
      key.key = sha1(str(user.id)).hexdigest() + tmp
      key.save()
      #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
  else:
    form = RememberPasswordForm()
  return my_render(request, 'seguridad/login/rememberPassword.html', {'form': form})

