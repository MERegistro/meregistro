from django.db import models

class Region(models.Model):
  nombre = models.CharField(max_length=50, unique=True)
  
  class Meta:
    app_label = 'registro'
