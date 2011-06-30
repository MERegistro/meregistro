# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from seguridad.models import Ambito
from seguridad.decorators import login_required
import simplejson as json


@login_required
def selector_ambito(request):
    result = []
    if request.GET.has_key('parent'):
        parentId = int(request.GET['parent'])
        ambitos = Ambito.objects.filter(parent=parentId)
    else:
        ambitos = Ambito.objects.filter(path__istartswith=request.get_perfil().ambito.path, level=request.get_perfil().ambito.level)
    ambitos = ambitos.filter(vigente=True)
    result += map(lambda a: {'id': a.id, 'descripcion': a.descripcion}, ambitos)
    return HttpResponse(json.dumps(result))
