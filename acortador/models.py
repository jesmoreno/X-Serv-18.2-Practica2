from django.db import models

# Create your models here.

class urlsStored (models.Model):
    pagina = models.TextField()
    numPagina = models.IntegerField()
