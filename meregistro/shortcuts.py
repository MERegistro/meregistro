from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.conf import settings


def my_render(request, template, context={}):
    context.update(csrf(request))
    context['STATIC_URL'] = settings.STATIC_URL
    context['flash'] = request.get_flash()
    context['user'] = request.user
    context['user_perfil'] = request.get_perfil()
    context['credenciales'] = set(request.get_credenciales())
    context['TESTING_MODE'] = settings.TESTING_MODE
    return render_to_response(template, context)
