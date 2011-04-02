# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'registro.views.index', name='home'),
    url(r'^establecimiento$', 'registro.views.establecimiento.index', name='establecimiento'),
    url(r'^establecimiento/([0-9]+)/edit', 'registro.views.establecimiento.edit', name='establecimientoEdit'),
    url(r'^establecimiento/create', 'registro.views.establecimiento.create', name='establecimientoCreate'),
)
