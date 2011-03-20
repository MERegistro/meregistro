# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from meregistro.shortcuts import my_render
from seguridad.decorators import login_required

@login_required
def index(request):
  return HttpResponse('hola' + request.get_perfil().rol.nombre)
