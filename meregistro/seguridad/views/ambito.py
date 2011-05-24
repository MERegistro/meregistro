# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from seguridad.models import Ambito
from seguridad.decorators import login_required
import simplejson as json


@login_required
def selector_ambito(request):
    if request.GET.has_key('parent'):
        ambitos = Ambito.objects.filter(parent=int(request.GET['parent']))
    else:
        ambitos = Ambito.objects.filter(level=0)
    result = map(lambda a: {'id': a.id, 'descripcion': a.descripcion}, ambitos)
    return HttpResponse(json.dumps(result))
