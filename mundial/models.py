from django.db import models

class Grupo(models.Model):
    nombre = models.CharField(max_length=1)

class Equipo(models.Model):
    bandera = models.ImageField(upload_to='cargas', null=True, blank=True)
    pais = models.CharField(max_length=100)
    golesF = models.IntegerField()
    golesC = models.IntegerField()
    partidosG = models.IntegerField()
    partidosP = models.IntegerField()
    empates = models.IntegerField()
    continente = models.CharField(max_length=100)
    grupo = models.ForeignKey(Grupo)

class Partido(models.Model):
    fase = models.CharField(max_length=1)
    hora = models.CharField(max_length=10)
    fecha = models.DateField()
    ganador = models.CharField(max_length=1)
    equipoL = models.ForeignKey(Equipo, related_name="Local")
    equipoV = models.ForeignKey(Equipo, related_name="Visitante")
    golesL = models.IntegerField()
    golesC = models.IntegerField()
