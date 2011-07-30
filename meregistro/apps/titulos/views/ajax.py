# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from apps.titulos.models import Titulo, EstadoTitulo
from apps.seguridad.models import Ambito
from apps.seguridad.decorators import login_required
import simplejson as json
from django.core import serializers


@login_required
def get_titulos_por_tipo(request, tipo_titulo_id):
    titulos = Titulo.objects.filter(jurisdicciones__id = request.get_perfil().jurisdiccion().id, estado__nombre = EstadoTitulo.VIGENTE, tipo_titulo = tipo_titulo_id)
    json_titulos = serializers.serialize("json", titulos)
    return HttpResponse(json_titulos, mimetype = "application/javascript")
