# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from apps.titulos.models import Titulo, EstadoTitulo, TituloJurisdiccional
from apps.seguridad.models import Ambito
from apps.seguridad.decorators import login_required
import simplejson as json
from django.core import serializers


@login_required
def get_titulos_por_tipo(request, tipo_titulo_id):
    titulos = Titulo.objects.filter(jurisdicciones__id = request.get_perfil().jurisdiccion().id, estado__nombre = EstadoTitulo.VIGENTE, tipo_titulo = tipo_titulo_id)
    json_titulos = serializers.serialize("json", titulos)
    return HttpResponse(json_titulos, mimetype = "application/javascript")

@login_required
def get_rango_anios_cohorte(request, titulo_jurisdiccional_id):
    titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk = titulo_jurisdiccional_id)
    anios = [i for i in range(titulo_jurisdiccional.datos_cohorte.get().anio_primera_cohorte, titulo_jurisdiccional.datos_cohorte.get().anio_ultima_cohorte + 1)]
    json_anios = json.dumps(anios)
    return HttpResponse(json_anios, mimetype = "application/javascript")

