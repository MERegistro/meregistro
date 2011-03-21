# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'seguridad.views.index', name='home'),
    url(r'^usuario$', 'seguridad.views.usuario.index', name='usuario'),
    url(r'^usuario/([0-9]+)/edit', 'seguridad.views.usuario.edit', name='usuarioEdit'),
)
