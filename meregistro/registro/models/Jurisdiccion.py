from django.db import models
from meregistro.registro.models import Region

class Jurisdiccion(models.Model):
  region = models.ForeignKey(Region)
  nombre = models.CharField(max_length=50)
  prefijo = models.IntegerField(null = True)

  class Meta:
    app_label = 'registro'
