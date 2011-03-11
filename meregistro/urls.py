from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login', 'seguridad.views.login', name='login'),
    url(r'^seleccionarPerfil', 'seguridad.views.seleccionarPerfil', name='seleccionarPerfil'),
    # Example:
    # (r'^meregistro/', include('meregistro.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)





