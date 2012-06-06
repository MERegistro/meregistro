# -*- coding: UTF-8 -*-

from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required

def index(request):
    return my_render(request, 'registro/index/index.html')
