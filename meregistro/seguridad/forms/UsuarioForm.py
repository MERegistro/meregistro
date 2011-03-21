from django.forms import ModelForm
from seguridad.models import Usuario

class UsuarioForm(ModelForm):
  class Meta:
    model = Usuario
