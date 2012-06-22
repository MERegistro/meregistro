from django.forms import ModelForm
from django import forms
from apps.seguridad.models import ConfiguracionSolapasAnexo


class ConfiguracionSolapasAnexoForm(ModelForm):
    class Meta:
        model = ConfiguracionSolapasAnexo
