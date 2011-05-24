# -*- coding: UTF-8 -*-
# Agrega al request propiedades asociadas a seguridad:
# * la propiedad user que referencia al usuario actual.

from seguridad.models import Usuario, Perfil


class LazyUser(object):
  def __get__(self, request, obj_type=None):
    if not hasattr(request, '_cached_user'):
      if request.session.has_key('user_id'):
        request._cached_user = Usuario.objects.get(pk=request.session['user_id'])
      else:
        request._cached_user = Usuario()
        request._cached_user.nombre = 'Anonimo'
    return request._cached_user


class SeguridadMiddleware(object):
  def process_request(self, request):
    assert hasattr(request, 'session'), "The seguridad authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
    request.__class__.user = LazyUser()

    def seleccionar_perfil(request, perfil_id):
      """
      Establece el perfil activo
      """
      perfil = Perfil.objects.get(pk=perfil_id)
      request.session['perfil_id'] = perfil_id
      # Cargar las credenciales del rol seleccionado
      request.session['credenciales'] = map(lambda c: c.nombre, perfil.rol.credenciales.all())
    request.__class__.seleccionar_perfil = seleccionar_perfil

    def get_perfil(request):
      """
      Retorna el perfil activo
      """
      if request.session.has_key('perfil_id'):
        return Perfil.objects.get(pk=request.session['perfil_id'])
      return None
    request.__class__.get_perfil = get_perfil

    def get_credenciales(request):
      """
      Retorna la lista de credenciales del perfil activo
      """
      if request.session.has_key('credenciales'):
        return request.session['credenciales']
      return []
    request.__class__.get_credenciales = get_credenciales

    def logout(request):
      """
      Retorna la lista de credenciales del perfil activo
      """
      if request.session.has_key('credenciales'):
        del request.session['credenciales']
      if request.session.has_key('user_id'):
        del request.session['user_id']
      if request.session.has_key('perfil_id'):
        del request.session['perfil_id']

    request.__class__.logout = logout

    return None
