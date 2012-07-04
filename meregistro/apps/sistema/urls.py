# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^ayuda$', 'apps.sistema.views.pages.ayuda', name = 'ayuda'),
)
