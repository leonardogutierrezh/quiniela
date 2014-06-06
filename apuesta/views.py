from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth.forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from social.models import *
from mundial.models import *
from apuesta.models import *
from apuesta.forms import *
from social.forms import *
from django.forms.formsets import formset_factory
import time
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.forms.formsets import formset_factory

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@login_required(login_url='/')
def resultados_grupo(request, id_grupo):
    if Configuracion.objects.get(tipo='apuestas').valor:
        usuario = request.user
        grupo = Grupo.objects.get(id=id_grupo)
        locales = Equipo.objects.filter(grupo=grupo)
        partidos = Partido.objects.filter(equipoL__id__in=locales)
        lista = []

        if request.method == 'POST':
            verificador = True
            for partido in partidos:
                equipoL = request.POST.get('resultado-' + str(partido.id) + '-' + str(partido.equipoL.id))
                equipoV = request.POST.get('resultado-' + str(partido.id) + '-' + str(partido.equipoV.id))

                if is_number(equipoL) and is_number(equipoV):
                    tupla = (partido,True,equipoL,equipoV)
                    lista.append(tupla)
                else:
                    tupla = (partido, False,0,0)
                    lista.append(tupla)
                    verificador = False
            if verificador:
                for partido in partidos:
                    equipoL = request.POST.get('resultado-' + str(partido.id) + '-' + str(partido.equipoL.id))
                    equipoV = request.POST.get('resultado-' + str(partido.id) + '-' + str(partido.equipoV.id))
                    if Apuesta.objects.filter(usuario=usuario, partido=partido):
                        apuesta = Apuesta.objects.get(usuario=usuario, partido=partido)
                        apuesta.golesL = equipoL
                        apuesta.golesV = equipoV
                        apuesta.save()
                    else:
                        apuesta = Apuesta.objects.create(partido=partido, golesL=equipoL, golesV=equipoV,
                                                         usuario=usuario, ganador='N')
                return HttpResponseRedirect('/mi_quiniela')
        else:
            for partido in partidos:
                if Apuesta.objects.filter(usuario=usuario, partido=partido):
                    apuesta = Apuesta.objects.get(usuario=usuario, partido=partido)
                    tupla = (partido, True,apuesta.golesL,apuesta.golesV)
                    lista.append(tupla)
                else:
                    tupla = (partido, True,0,0)
                    lista.append(tupla)

        return render_to_response('apuesta/resultados_grupo.html', {'partidos':lista, 'grupo': grupo}, context_instance=RequestContext(request))
    return HttpResponseRedirect('/ver_grupo/' + id_grupo)