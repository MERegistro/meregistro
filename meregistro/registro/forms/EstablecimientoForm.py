from django.forms import ModelForm
from registro.models import Establecimiento

class EstablecimientoForm(ModelForm):

  class Meta:
    model = Establecimiento
