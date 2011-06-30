# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'apps.titulos.views.titulo.index', name = 'home'),
    url(r'^index$', 'apps.titulos.views.titulo.index', name = 'titulo'),
)
