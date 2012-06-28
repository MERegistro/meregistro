from django.forms import ModelForm
from django import forms
from apps.backend.models import ConfiguracionSolapasEstablecimiento


class ConfiguracionSolapasEstablecimientoForm(ModelForm):
    class Meta:
        model = ConfiguracionSolapasEstablecimiento
