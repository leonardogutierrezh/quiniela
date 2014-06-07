from django.contrib import admin
from mundial.models import *
from apuesta.models import *
from social.models import *

admin.site.register(Grupo)
admin.site.register(Equipo)
admin.site.register(Partido)
admin.site.register(Torneo)
admin.site.register(Invitacion)
admin.site.register(Apuesta)
admin.site.register(Configuracion)
admin.site.register(ConfiguracionPuntos)
admin.site.register(Puntaje)