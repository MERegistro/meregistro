from django.forms import ModelForm
from django import forms
from apps.seguridad.models import ConfiguracionSolapasEstablecimiento


class ConfiguracionSolapasEstablecimientoForm(ModelForm):
    class Meta:
        model = ConfiguracionSolapasEstablecimiento
