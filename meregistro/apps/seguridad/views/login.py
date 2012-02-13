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
from django.core.mail import EmailMessage
from meregistro import settings

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
          #user.update_last_login()
          request.session['user_id'] = user.id
          user.update_last_login()
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
      user = Usuario.objects.filter(documento=form.cleaned_data['documento']).filter(tipo_documento=form.cleaned_data['tipo_documento']).all()[0]
      key = PasswordRememberKey()
      key.usuario = user
      tmp = ''.join(random.sample("1234567890qwertyuiopasdfghjklzxcvbnm", 32))
      key.key = sha1(str(user.id)).hexdigest() + tmp
      key.save()
      html_content = 'Haga click en el siguiente link para resetear su contraseña:'
      html_content += '<a href="'+settings.BASE_URL+'reset_password/'+key.key+'">Resetear contraseña</a>'
      msg = EmailMessage("Recordatorio de contraseña", html_content, settings.EMAIL_FROM, [user.email])
      msg.content_subtype = "html"  # Main content is now text/html
      msg.send()
      request.set_flash('success', 'Se le ha enviado un mail con instrucciones a ' + user.email + ' para volver a acceder al sistema.')
  else:
    init = {}
    try:
        init['tipo_documento'] = TipoDocumento.objects.get(abreviatura='DNI').id
    except:
        pass
    form = RememberPasswordForm(init)
  return my_render(request, 'seguridad/login/rememberPassword.html', {'form': form})

def reset_password(request, key):
    try:
        prk = PasswordRememberKey.objects.get(key=key)
        new_pass = ''.join(random.sample("1234567890qwertyuiopasdfghjklzxcvbnm", 8))
        prk.usuario.set_password(new_pass)
        user = prk.usuario
        user.save()
        prk.delete()
        html_content = 'Su nueva contraseña es: '+new_pass+'<br />'
        html_content += 'Haga click en el siguiente link para ingresar al sistema:'
        html_content += '<a href="'+settings.BASE_URL+'">Ingresar al sistema</a>'
        msg = EmailMessage("Nueva contraseña", html_content, settings.EMAIL_FROM, [user.email])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        request.set_flash('success', 'Se le ha enviado un mail con su nueva contraseña para volver a acceder al sistema.')
    except:
      request.set_flash('warning', 'Link inválido')
    return my_render(request, 'seguridad/login/resetPassword.html', {})
