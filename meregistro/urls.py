from django.conf.urls.defaults import *
from django.conf import settings
import seguridad.urls
import registro.urls

urlpatterns = patterns('',
    url(r'^login', 'seguridad.views.login', name='login'),
    url(r'^logout', 'seguridad.views.logout', name='logout'),
    url(r'^seguridad/', include(seguridad.urls)),
    url(r'^registro/', include(registro.urls)),
    url(r'^seleccionarPerfil', 'seguridad.views.seleccionar_perfil', name='seleccionarPerfil'),
    url(r'^' + settings.STATIC_URL_PATH + '/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    url(r'^$', 'registro.views.index', name="index"),
)

