from django.forms import ModelForm
from apps.seguridad.models import Rol


class RolForm(ModelForm):
    class Meta:
        model = Rol
        exclude = ('credenciales', 'roles_asignables')
