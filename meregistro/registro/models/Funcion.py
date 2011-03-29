from django.db import models

class Funcion(models.Model):
  nombre = models.CharField(max_length=255, unique=True)

  class Meta:
    app_label = 'registro'
