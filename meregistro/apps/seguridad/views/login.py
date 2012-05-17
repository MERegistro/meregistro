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
  if request.method == 'POST' and len(request.POST) > 0:
    form = RememberPasswordForm(request.POST)
    if form.is_valid():
      user = Usuario.objects.filter(documento=form.cleaned_data['documento']).filter(tipo_documento=form.cleaned_data['tipo_documento']).all()[0]
      key = PasswordRememberKey()
      key.usuario = user
      tmp = ''.join(random.sample("1234567890qwertyuiopasdfghjklzxcvbnm", 32))
      key.key = sha1(str(user.id)).hexdigest() + tmp
      key.save()
      html_content = u"""
Hola """ + user.nombre + u" " + user.apellido + u""",<br />
Hemos recibido recientemente una solicitud para restablecer su contraseña.
Si usted no solicitó el restablecimiento, simplemente ignore este mensaje.
Si efectivamente es usted quien lo solicitó, por favor haga clic en el enlace que se encuentra más abajo y
nosotros le enviaremos, en otro correo, la nueva contraseña para acceder al sistema.<br /><br />
<a href=\""""+settings.BASE_URL+"""reset_password/"""+key.key+u"""\">Enviarme una Nueva Contraseña</a>
<br /><br />
Muchas gracias,<br />
Registro Federal de Instituciones y Ofertas de Formación Docente
      """
      msg = EmailMessage("Confirmación de Solicitud de Restablecimiento de Contraseña", html_content, settings.EMAIL_FROM, [user.email])
      msg.content_subtype = "html"  # Main content is now text/html
      msg.send()
      request.set_flash('success', u'Le hemos enviado a ' + user.email + u' instrucciones para restablecer su contraseña y volver a tener acceso al sistema. Tenga en cuenta que tal vez deba revisar la carpeta de Spam para leer el correo. para volver a acceder al sistema.')
  else:
    init = {}
    try:
        init['tipo_documento'] = TipoDocumento.objects.get(abreviatura='DNI').id
    except:
        pass
    form = RememberPasswordForm(initial=init)
  return my_render(request, 'seguridad/login/rememberPassword.html', {'form': form})

def reset_password(request, key):
  try:
    prk = PasswordRememberKey.objects.get(key=key)
    new_pass = ''.join(random.sample("1234567890qwertyuiopasdfghjklzxcvbnm", 8))
    prk.usuario.set_password(new_pass)
    user = prk.usuario
    user.save()
    prk.delete()
    html_content = u"""Hola """ + user.nombre + " " + user.apellido + u""",<br />
    Le informamos que su nueva contraseña de acceso al sistema REFFOD es: """ + new_pass + u"""<br /><br />
    Si lo considera apropiado, una vez que haya ingresado al sistema utilizando esta contraseña, podrá cambiarla
    haciendo clic en el menú <b>MIS DATOS</b>, en la opción <b>Modificar contraseña</b>.<br /><br />
    Si desea acceder ahora, haga clic en el siguiente enlace:<br />
    <a href=\""""+settings.BASE_URL+u"""\">Acceder al Sistema REFFOD</a>
    Muchas gracias,
    Registro Federal de Instituciones y Ofertas de Formación Docente
    """
    msg = EmailMessage(u"Nueva Contraseña de Acceso al REFFOD", html_content, settings.EMAIL_FROM, [user.email])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    request.set_flash('success', u'Le hemos enviado a ' + user.email + u' la nueva contraseña de acceso al sistema. Tenga en cuentaque tal vez deba revisar la carpeta de Spam para leer el correo.')
  except:
    request.set_flash('warning', 'Link inválido')
  return my_render(request, 'seguridad/login/resetPassword.html', {})
