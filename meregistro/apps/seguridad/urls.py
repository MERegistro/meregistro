# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'apps.seguridad.views.index', name='seguridadHome'),
    url(r'^usuario$', 'apps.seguridad.views.usuario.index', name='usuario'),
    url(r'^usuario/([0-9]+)/edit', 'apps.seguridad.views.usuario.edit', name='usuarioEdit'),
    url(r'^usuario/([0-9]+)/changePassword', 'apps.seguridad.views.usuario.change_password', name='usuarioChangePassword'),
    url(r'^usuario/create', 'apps.seguridad.views.usuario.create', name='usuarioCreate'),
    url(r'^usuario/([0-9]+)/bloquear', 'apps.seguridad.views.usuario.bloquear', name='usuarioBloquear'),
    url(r'^usuario/([0-9]+)/desbloquear', 'apps.seguridad.views.usuario.desbloquear', name='usuarioDesbloquear'),
    url(r'^usuario/([0-9]+)/verPerfiles', 'apps.seguridad.views.perfil.verPerfilesUsuario', name='verPerfilesUsuario'),
    url(r'^usuario/([0-9]+)/asignarPerfil', 'apps.seguridad.views.perfil.create', name='asignarPerfilUsuario'),
    url(r'^ambito/selector', 'apps.seguridad.views.ambito.selector_ambito', name='selectorAmbito'),
)
