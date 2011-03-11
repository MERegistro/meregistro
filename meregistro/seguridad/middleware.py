# -*- coding: UTF-8 -*-
# Agrega al request propiedades asociadas a seguridad:
# * la propiedad user que referencia al usuario actual.

from seguridad.models import Usuario

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
    return None
