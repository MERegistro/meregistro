from django.forms import ModelForm
from django import forms
from apps.seguridad.models import ConfiguracionSolapasExtensionAulica

class ConfiguracionSolapasExtensionAulicaForm(ModelForm):
    class Meta:
        model = ConfiguracionSolapasExtensionAulica
