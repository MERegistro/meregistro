# -*- coding: UTF-8 -*-

from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required

def index(request):
    if request.user.is_authenticated():
        extend_template = 'base_registro.html'
    else:
        extend_template = 'base.html'
    return my_render(request, 'registro/index/index.html', {
        'extend_template': extend_template
    })
