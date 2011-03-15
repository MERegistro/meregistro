from functools import update_wrapper, wraps
from django.http import HttpResponseRedirect

def login_required(view):
  @wraps(view)
  def wrapper(request, *args, **kwargs):
    if not request.user.is_authenticated():
      return HttpResponseRedirect('/login?login_required')
    return view(request, *args, **kwargs)
  return wrapper
