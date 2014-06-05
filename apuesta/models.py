from django.db import models
from django.contrib.auth.models import User
from mundial.models import *

class Apuesta(models.Model):
    partido = models.ForeignKey(Partido)
    golesL = models.IntegerField()
    golesV = models.IntegerField()
    usuario = models.ForeignKey(User)
    ganador = models.CharField(max_length=1)