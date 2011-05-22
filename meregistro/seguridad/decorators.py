from functools import wraps
from django.http import HttpResponseRedirect


def login_required(view):
    """
    Chequea que el usuario este logueado.
    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login?login_required')
        return view(request, *args, **kwargs)
    return wrapper


def credential_required(credential):
    """
    Chequea que el usuario este logueado y el rol del perfil que selecciono
    tenga la credencial credential.
    """
    def check_credential(view):
        @login_required
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if credential not in request.get_credenciales():
                return HttpResponseRedirect('/secure')
            return view(request, *args, **kwargs)
        return wrapper
    return check_credential
