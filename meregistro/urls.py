from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^login', 'seguridad.views.login', name='login'),
    url(r'^seguridad/', 'seguridad.views.index', name='seguridadHome'),
    url(r'^seleccionarPerfil', 'seguridad.views.seleccionarPerfil', name='seleccionarPerfil'),
    url(r'^' + settings.STATIC_URL_PATH + '/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    url(r'^$', 'registro.views.index', name="index"),
)

