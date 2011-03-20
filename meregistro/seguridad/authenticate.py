from hashlib import sha1
from seguridad.models import Usuario

def encrypt_password(usuario, password):
  """
  Encripta una password para el Usuario usuario.

  @param Usuario usuario.
  @param string password.
  @return string password encriptada.
  """
  return sha1(password).hexdigest()

def authenticate(tipo_documento, documento, password):
  """
  Autentica un usuario a partir de sus credenciales de acceso
  
  @param TipoDocumento tipo de documento del usuario.
  @param string documento documento del usuario.
  @param string password password del usuario.
  @return Usuario|boolean False si las credenciales de acceso no son validas o
  el objeto Usuario en caso que si lo sean.
  """
  try:
    user = Usuario.objects.get(tipo_documento=tipo_documento, documento=documento)
    if user.password == encrypt_password(user, password):
      return user
    return False
  except Usuario.DoesNotExist:
    return False
  
