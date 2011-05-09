# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from seguridad.models import Ambito
from seguridad.decorators import login_required
from json.encoder import JSONEncoder

@login_required
def selector_ambito(request):
	if request.GET.has_key('parent'):
		ambitos = Ambito.objects.filter(parent=int(request.GET['parent']))
	else:
		ambitos = Ambito.objects.filter(level=0)
	encoder = JSONEncoder()
	result = map(lambda a: {'id': a.id, 'descripcion': a.descripcion }, ambitos)
	return HttpResponse(encoder.encode(result))
