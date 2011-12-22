# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *
from apps.registro.models.Establecimiento import Establecimiento

urlpatterns = patterns('',
    url(r'^establecimientos$', 'apps.reportes.views.establecimiento.establecimientos', name='reporteEstablecimientos'),
)
