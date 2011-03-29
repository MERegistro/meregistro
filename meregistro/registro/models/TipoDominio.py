from django.db import models

class TipoDominio(models.Model):
  descripcion = models.CharField(max_length=50, unique=True)

  class Meta:
    app_label = 'registro'
