# -*- coding: UTF-8 -*-


from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.reportes.models.Estadistica import Estadistica
from django.core.paginator import Paginator

ITEMS_PER_PAGE = 100000



@login_required
@credential_required('consulta_estadistica_nacional')
def datos_generales(request):
    rows = Estadistica.datos_generales()
    paginator = Paginator(rows, ITEMS_PER_PAGE)
    
    try:
        page_number = int(request.GET['page'])
    except (KeyError, ValueError):
        page_number = 1
    # chequear los límites
    if page_number < 1:
        page_number = 1
    elif page_number > paginator.num_pages:
        page_number = paginator.num_pages

    page = paginator.page(page_number)
    rows = page.object_list
	
	
    return my_render(request, 'reportes/estadistica/datos_generales.html', {
	    'rows': rows,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
	})


def datos_basicos_sede(request):
    rows = Estadistica.datos_basicos_sede()
    raise Exception(rows)
