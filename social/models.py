from django.db import models
from django.contrib.auth.models import User

class Torneo(models.Model):
    nombre = models.CharField(max_length=200)
    administrador = models.ForeignKey(User, related_name="administrador")
    miembros = models.ManyToManyField(User)

class Invitacion(models.Model):
    correo = models.EmailField()
    torneo = models.ForeignKey(Torneo)
    hash = models.CharField(max_length=100)
