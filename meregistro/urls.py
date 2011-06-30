from django.conf.urls.defaults import *
from django.conf import settings
import apps.seguridad.urls
import apps.registro.urls
import apps.titulos.urls

urlpatterns = patterns('',
    url(r'^login', 'apps.seguridad.views.login', name='login'),
    url(r'^logout', 'apps.seguridad.views.logout', name='logout'),
    url(r'^seguridad/', include(apps.seguridad.urls)),
    url(r'^registro/', include(apps.registro.urls)),
    url(r'^titulos/', include(apps.titulos.urls)),
    url(r'^seleccionarPerfil', 'apps.seguridad.views.seleccionar_perfil', name='seleccionarPerfil'),
    url(r'^' + settings.STATIC_URL_PATH + '/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    url(r'^$', 'apps.registro.views.index', name="index"),
)

