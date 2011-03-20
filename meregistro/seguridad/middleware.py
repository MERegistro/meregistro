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
      perfil = Perfil.objects.get(pk = perfil_id)
      request.session['perfil_id'] = perfil_id
    request.__class__.seleccionar_perfil = seleccionar_perfil

    def get_perfil(request):
      """
      Retorna el perfil activo
      """
      return Perfil.objects.get(pk = request.session['perfil_id'])
    request.__class__.get_perfil = get_perfil

    return None
