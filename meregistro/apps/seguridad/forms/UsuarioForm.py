from django.forms import ModelForm
from apps.seguridad.models import Usuario


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
