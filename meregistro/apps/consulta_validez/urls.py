# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'apps.consulta_validez.views.index', name='consultaValidezHome'),
    url(r'^([0-9]+)/detalle$', 'apps.consulta_validez.views.detalle', name='consultaValidezDetalle'),
   )
