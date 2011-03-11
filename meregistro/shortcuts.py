from django.shortcuts import render_to_response
from django.core.context_processors import csrf

def my_render(request, template, context):
  context.update(csrf(request))
  return render_to_response(template, context)  
