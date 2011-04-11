# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'seguridad.views.index', name='seguridadHome'),
    url(r'^usuario$', 'seguridad.views.usuario.index', name='usuario'),
    url(r'^usuario/([0-9]+)/edit', 'seguridad.views.usuario.edit', name='usuarioEdit'),
    url(r'^usuario/([0-9]+)/changePassword', 'seguridad.views.usuario.change_password', name='usuarioChangePassword'),
    url(r'^usuario/create', 'seguridad.views.usuario.create', name='usuarioCreate'),
    url(r'^usuario/([0-9]+)/bloquear', 'seguridad.views.usuario.bloquear', name='usuarioBloquear'),
    url(r'^usuario/([0-9]+)/desbloquear', 'seguridad.views.usuario.desbloquear', name='usuarioDesbloquear'),
    url(r'^usuario/([0-9]+)/verPerfiles', 'seguridad.views.perfil.verPerfilesUsuario', name='verPerfilesUsuario'),
    url(r'^usuario/([0-9]+)/asignarPerfil', 'seguridad.views.perfil.create', name='asignarPerfilUsuario'),
)
