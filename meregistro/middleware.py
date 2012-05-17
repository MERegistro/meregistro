# -*- coding: UTF-8 -*-

class FlashMiddleware:
  """
  Agrega los metodos set_flash y get_flash al request.
  """

  def process_request(self, request):
    if not request.session.has_key('flash'):
      request.session['flash'] = None
    
    def set_flash(request, flash_type, flash_msg):
      request.session['flash'] = {'type': flash_type, 'message': flash_msg}
    request.__class__.set_flash = set_flash

    def get_flash(request):
      flash = request.session['flash']
      request.session['flash'] = None
      return flash
    request.__class__.get_flash = get_flash
