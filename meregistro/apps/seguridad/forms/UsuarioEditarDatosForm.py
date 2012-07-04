# -*- coding: UTF-8 -*-

from django import forms
from apps.seguridad.models import Usuario


class UsuarioEditarDatosForm(forms.ModelForm):
#    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='contraseña')
#    repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='Repetir contraseña')

    class Meta:
        model = Usuario
        exclude = ('tipo_documento', 'documento', 'password', 'last_login', 'is_active')
